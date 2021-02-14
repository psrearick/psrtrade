import backtrader as bt
import helpers.Logger as logger


class FastCross(bt.Strategy):
    params = (
        ('fast', 5),
        ('slow', 20),
    )

    def __init__(self):
        self.logger = logger.Logger()
        self.indicators = dict()
        for i, d in enumerate(self.datas):
            if (i + 1) == len(self.datas): continue
            next_data = self.datas[i + 1]
            if not d._name + '_long' == next_data._name: continue
            self.indicators[d] = dict()
            inds = self.indicators[d]
            inds['close'] = d.close
            inds['fast_moving_average'] = bt.indicators.SMA(
                d.close, period=self.p.fast, plotname=str(self.p.fast) + '-Period SMA')
            inds['slow_moving_average'] = bt.indicators.SMA(
                d.close, period=self.p.slow, plotname=str(self.p.slow) + '-Period SMA')
            inds['crossover'] = bt.indicators.CrossOver(
                inds['fast_moving_average'], inds['slow_moving_average'])

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            # print('ORDER SUBMITTED')
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                pass
                print(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            else:  # Sell
                self.stop_loss = 0
                self.profit = 0
                print('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print('Order {}'.format(order.status))

    def prenext(self):
        self.next()

    def next(self):
        pass
        for i, d in enumerate(self.datas):
            if d not in self.indicators.keys():
                continue
            inds = self.indicators[d]
            dt, dn = self.datetime.date(), d._name
            pos = self.getposition(d).size
            if len(inds['crossover']) < 1:
                continue
            if pos == 0:
                if inds['crossover'][0] > 0:
                    o = self.buy(data=d, exectype=bt.Order.Market)

            if pos > 0:
                if inds['crossover'][0] < 0:
                    self.close(data=d)
