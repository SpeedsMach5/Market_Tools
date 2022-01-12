import backtrader as bt
import datetime
from pandas.core.frame import DataFrame 
from ema_sma_crossover_strategyt import MA_CrossOver
import matplotlib as plot
import yfinance as yf
import pandas as pd
from datetime import date
import matplotlib
matplotlib.use('agg')

def buy_the_dip(pricing_data:DataFrame):
    df = pricing_data.set_index('Date')
    cerebro = bt.Cerebro()

    cerebro.addstrategy(MA_CrossOver)
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)
    cerebro.broker.set_cash(100000)
    cerebro.addsizer(bt.sizers.FixedSize, stake=500)

    beginning_balance = float(cerebro.broker.getvalue())
    cerebro.run()
    ending_balance = float(cerebro.broker.getvalue())
    plot = cerebro.plot()[0][0]

    return df, [beginning_balance, ending_balance], plot
