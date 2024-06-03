import datetime
import math
from typing import final
import backtrader as bt
import os

from backtrader.dataseries import TimeFrame
from tutorial_strategy import TestStrategy
os.system('color a')

class MaxSizer(bt.Sizer):
    share_num = 0
    def _getsizing(self, comminfo, cash, data, isbuy):
        
        position = self.broker.getposition(data)
        if isbuy:
            size = math.floor((cash/data))
            MaxSizer.share_num = size
            print(f'BOUGHT {size} shares at ${data.tick_last}')
        elif not isbuy and not position.size:
            return 0
        elif not isbuy:
            size = MaxSizer.share_num
            print(f'SOLD {size} shares at ${data.tick_last}')
            MaxSizer.share_num = 0
        return size

cerebro = bt.Cerebro()

cerebro.broker.setcash(100000.0)
initial_cash = cerebro.broker.getvalue()

data = bt.feeds.YahooFinanceCSVData(
#data = bt.feeds.GenericCSVData(
    dataname='D:\Desktop Backup\School\Homework\Statistics\Python Stuff\Backtrader\oracle_data.csv',
    #dataname='D:\Desktop Backup\School\Homework\Statistics\Python Stuff\Backtrader\AAPL_1hour_sample.csv',
    # Do not pass values before this date
    fromdate=datetime.datetime(2000, 1, 1),
    # Do not pass values after this date
    todate=datetime.datetime(2006, 12, 31),
    reverse=False)

#data = bt.feeds.GenericCSVData(dataname='D:\Desktop Backup\School\Homework\Statistics\Python Stuff\Backtrader\AAPL_1hour_sample.csv',
#                                   timeframe=bt.TimeFrame.Minutes,
#                                  fromdate = datetime.datetime(2021,1,4),
#                                  todate=datetime.datetime(2021,1,14),
#                                  dtformat=('%Y-%m-%d'),
#                                  tmformat=('%H:%M:%S'),
#                                  datetime=0,
#                                  time=1,
#                                  open=2,
#                                  high=3,
#                                  low=4,
#                                  close=5,
#                                  volume=6,
#                                  openinterest=-1)

cerebro.adddata(data)
cerebro.addstrategy(TestStrategy)
cerebro.addsizer(MaxSizer)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())


cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
final_cash = cerebro.broker.cash
print('You bought %d orders\n' %TestStrategy.buy_count)
print('You sold %d orders\n' %TestStrategy.sell_count)
print(f'You had {TestStrategy.wins} wins and {TestStrategy.losses} losses\n')
print(f'You have ${final_cash-initial_cash:0.2f} in cash, which is a {100*((final_cash-initial_cash)/initial_cash):0.2f}% change.')
print(f'You have ${cerebro.broker.getvalue()-initial_cash:0.2f} in portfolio value, which is a {100*((cerebro.broker.getvalue()-initial_cash)/initial_cash):0.2f}% change.')
cerebro.plot(plotter=None, style = 'candle', barup = 'green')
input()