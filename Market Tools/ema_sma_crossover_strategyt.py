# Create a EMA/SMA Crossover strategy


from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import backtrader as bt
import backtrader.indicators as btind


def EMA():
    with open("data/MA_periods.txt", "r") as file:
        content = file.read()
        content = content.split("\n")
        return content

fast_period = EMA() 

def SMA():
    with open("data/MA_periods.txt", "r") as file:
        content = file.read()
        content = content.split("\n")
        return content

slow_period = SMA()
  

class MA_CrossOver(bt.Strategy):
    
    alias = ('SMA_CrossOver',)

    params = (
        # period for the fast Moving Average
        ('fast',10),
        # period for the slow moving average
        ('slow',30),
        # period for the slow moving average
        ('slow',20),
        # moving average to use
        ('_movav', btind.MovAv.SMA(20,30).EMA(10))
    )

    def __init__(self):
        sma_fast = self.p._movav(period=self.p.fast)
        sma_slow = self.p._movav(period=self.p.slow)

        self.buysig = btind.CrossOver(sma_fast, sma_slow)

    def next(self):
        if self.position.size:
            if self.buysig < 0:
                self.sell()

        elif self.buysig > 0:
            self.buy()

    