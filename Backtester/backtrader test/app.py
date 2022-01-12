import backtrader as bt
import datetime 
from ema_sma_crossover_strategyt import MA_CrossOver
from dip_buy_strategy import TestStrategy
import matplotlib as plot


cerebro = bt.Cerebro()

cerebro.broker.set_cash(1000000)



data = bt.feeds.YahooFinanceCSVData(
    dataname="oracle.csv",
    # Do not pass values before this date
    fromdate=datetime.datetime(2000, 1, 1),
    # Do not pass values after this date
    todate=datetime.datetime(2000, 12, 31),
    reverse=False)

cerebro.adddata(data)
cerebro.broker.set_cash(1000000)
cerebro.addstrategy(MA_CrossOver)
#cerebro.addstrategy(TestStrategy)
cerebro.addsizer(bt.sizers.FixedSize, stake=10000)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

#cerebro.plot()

