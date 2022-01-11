# Import the required libraries
import numpy as np
import pandas as pd
import hvplot.pandas
from pathlib import Path
from datetime import date
from pandas.core.frame import DataFrame
import yfinance as yf
import os
import pricing

def analyze_macd(signals_df:DataFrame):
  # Calculate the MACD and Signal Line Indicators
  # Calculate the short term exponential moving average (EMA)
  signals_df["short_ema"] = signals_df.Close.ewm(span=12, adjust=False).mean()

  # Calculate the long term exponential moving average (EMA)
  signals_df["long_ema"] = signals_df.Close.ewm(span=26, adjust=False).mean()

  # Calculate the MACD Line
  signals_df["macd"] = signals_df["short_ema"] - signals_df["long_ema"]

  # Calculate the Signal Line
  signals_df["signal line"] = signals_df["macd"].ewm(span=9, adjust=False).mean()

  # Create a column to hold the trading signal
  signals_df["Signal"] = 0.0
  
  # Generate the trading signal 0 or 1,
  # where 1 is the MACD greater than the signal line
  # and 0 is when the condition is not met
  signals_df["Signal"] = np.where(
      signals_df["macd"] > signals_df["signal line"], 1.0, 0.0
  )

  # Calculate the points in time when the Signal value changes
  # Identify trade entry (1) and exit (-1) points
  signals_df["Entry/Exit"] = signals_df["Signal"].diff()

  # Review the DataFrame
  # signals_df.loc["2015-12-03":"2015-12-13"]

  # Visualize exit position relative to close price
  exit = signals_df[signals_df['Entry/Exit'] == -1.0]['Close'].hvplot.scatter(
      color="yellow",
      marker="v",
      size=200,
      legend=False,
      ylabel="Price in $",
      width=1000,
      height=400)

  # Visualize entry position relative to close price
  entry = signals_df[signals_df['Entry/Exit'] == 1.0]['Close'].hvplot.scatter(
      color="purple",
      marker="^",
      size=200,
      legend=False,
      ylabel="Price in $",
      width=1000,
      height=400)

  # Visualize close price for the investment
  security_close = signals_df[['Close']].hvplot(
      line_color="lightgray",
      ylabel="Price in $",
      width=1000,
      height=400)

  # Visualize moving averages
  dmac_signal_lines = signals_df[["macd", "signal line"]].hvplot(
      ylabel="Price in $",
      width=1000,
      height=400)

  # Create the overlay plot
  entry_exit_plot = security_close * dmac_signal_lines * entry * exit

  return signals_df, entry_exit_plot

def backtest_macd(signals_df):
  # Set initial capital
  initial_capital = float(100000)

  # Set the share size
  share_size = 500

  # Buy a 500 share position when the dual moving average crossover Signal equals 1 (SMA50 is greater than SMA100)
  # Sell a 500 share position when the dual moving average crossover Signal equals 0 (SMA50 is less than SMA100)
  signals_df['Position'] = share_size * signals_df['Signal']

  # Determine the points in time where a 500 share position is bought or sold
  signals_df['Entry/Exit Position'] = signals_df['Position'].diff()

  # Multiply the close price by the number of shares held, or the Position
  signals_df['Portfolio Holdings'] = signals_df.Close * signals_df['Position']

  # Subtract the amount of either the cost or proceeds of the trade from the initial capital invested
  signals_df['Portfolio Cash'] = initial_capital - (signals_df.Close * signals_df['Entry/Exit Position']).cumsum()

  # Calculate the total portfolio value by adding the portfolio cash to the portfolio holdings (or investments)
  signals_df['Portfolio Total'] = signals_df['Portfolio Cash'] + signals_df['Portfolio Holdings']

  # Calculate the portfolio daily returns
  signals_df['Portfolio Daily Returns'] = signals_df['Portfolio Total'].pct_change()

  # Calculate the portfolio cumulative returns
  signals_df['Portfolio Cumulative Returns'] = (1 + signals_df['Portfolio Daily Returns']).cumprod() - 1

  # Visualize exit position relative to total portfolio value
  exit = signals_df[signals_df['Entry/Exit'] == -1.0]['Portfolio Total'].hvplot.scatter(
      color='yellow',
      marker='v',
      size=200,
      legend=False,
      ylabel='Total Portfolio Value',
      width=1000,
      height=400
  )

  # Visualize entry position relative to total portfolio value
  entry = signals_df[signals_df['Entry/Exit'] == 1.0]['Portfolio Total'].hvplot.scatter(
      color='purple',
      marker='^',
      size=200,
      ylabel='Total Portfolio Value',
      width=1000,
      height=400
  )

  # Visualize the value of the total portfolio
  total_portfolio_value = signals_df[['Portfolio Total']].hvplot(
      line_color='lightgray',
      ylabel='Total Portfolio Value',
      xlabel='Date',
      width=1000,
      height=400
  )

  # Overlay the plots
  portfolio_entry_exit_plot = total_portfolio_value * entry * exit
  portfolio_entry_exit_plot.opts(
      title="Total Portfolio Value",
      yformatter='%.0f'
  )

  return signals_df[["Portfolio Total", "Portfolio Cumulative Returns"]], portfolio_entry_exit_plot