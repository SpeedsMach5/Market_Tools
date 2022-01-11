# Import the required libraries
import numpy as np
import pandas as pd
import hvplot
from pathlib import Path
from datetime import date
from pandas.core.frame import DataFrame
import yfinance as yf
import os
import pricing

def analyze_dmac(signals_df:DataFrame):
    short_window = 50
    long_window = 100
    signals_df["SMA50"] = signals_df.Close.rolling(window=short_window).mean()
    signals_df["SMA100"] = signals_df.Close.rolling(window=long_window).mean()
    signals_df["Signal"] = 0.0
    signals_df["Signal"][short_window:] = np.where(
        signals_df["SMA50"][short_window:] > signals_df["SMA100"][short_window:], 1.0, 0.0
    )

    # Calculate the points in time when the Signal value changes
    # Identify trade entry (1) and exit (-1) points
    signals_df["Entry/Exit"] = signals_df["Signal"].diff()

    # Review the DataFrame
    # signals_df.loc["2015-12-03":"2015-12-13"]

    exit = signals_df[signals_df['Entry/Exit'] == -1.0]['Close'].hvplot.scatter(
        color="red",
        marker="v",
        size=200,
        legend=False,
        ylabel="Price in $",
        width=1000,
        height=400)
    
    entry = signals_df[signals_df['Entry/Exit'] == 1.0]['Close'].hvplot.scatter(
        color="green",
        marker="^",
        size=200,
        legend=False,
        ylabel="Price in $",
        width=1000,
        height=400)

    security_close = signals_df[['Close']].hvplot(
        line_color="black",
        ylabel="Price in $",
        width=1000,
        height=400)

    moving_avgs = signals_df[["SMA50", "SMA100"]].hvplot(
        ylabel="Price in $",
        width=1000,
        height=400)

    entry_exit_plot = security_close * moving_avgs * entry * exit

    return signals_df, entry_exit_plot

def backtest_dmac(signals_df):
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