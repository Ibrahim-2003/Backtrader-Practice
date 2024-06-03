import backtrader as bt
class TestStrategy(bt.Strategy):
    cerebro = bt.Cerebro()
    #size = bt.Sizer
    buy_count = 0
    sell_count = 0
    account_money = cerebro.broker.getvalue()
    buy_stock = 1
    buy_price = 0
    wins = 0
    losses = 0

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.datalow = self.datas[0].low
        TestStrategy.buy_stock = int(TestStrategy.account_money / self.dataclose[0])
        TestStrategy.buy_price = self.dataclose[0]
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        # Write down: no pending order
        self.order = None


    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            #Add a golden cross (50 day ma surpasses the 200 day ma)
            #Look into the death cross (200 day ma surpasses the 50 day ma)

            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close

                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    TestStrategy.buy_count += 1
                    self.buy()
        else:
            if self.dataclose[0] >= 1.001*self.dataclose[-1]:
                sell_winning = self.dataclose[0] - TestStrategy.buy_price
                self.log(f'SOLD, {self.dataclose[0]:0.2f}, WINNING: {sell_winning:0.2f}')
                if sell_winning > 0:
                    TestStrategy.wins += 1
                elif sell_winning <= 0:
                    TestStrategy.losses += 1
                TestStrategy.sell_count += 1
                self.sell()
                #for data in self.datas:
                #    size=self.getposition(data).size
                #    if  size!=0:
                #        self.close(data)