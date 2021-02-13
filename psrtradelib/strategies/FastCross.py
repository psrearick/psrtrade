import math
import backtrader as bt

class FastCross(bt.Strategy):

    params = (
        ('fast', 5),
        ('slow', 20),
    )

    def __init__(self):
        self.indicators = dict()
        for i, d in enumerate(self.datas):
            if (i + 1) == len(self.datas): continue
            next_data = self.datas[i + 1]
            if not d._name + '_long' == next_data._name: continue
            self.indicators[d] = dict()
            inds = self.indicators[d]
            inds['fast_moving_average'] = bt.indicators.SMA(
                d.close, period=self.p.fast, plotname=str(self.p.fast) + '-Period SMA')
            inds['slow_moving_average'] = bt.indicators.SMA(
                d.close, period=self.p.slow, plotname=str(self.p.slow)+'-Period SMA')
            inds['crossover'] = bt.indicators.CrossOver(
                inds['fast_moving_average'], inds['slow_moving_average'])

    def next(self):
        for i, d in enumerate(self.datas):
            if not d in self.indicators.keys(): continue
            inds = self.indicators[d]
            dt, dn = self.datetime.date(), d._name
            pos = self.getposition(d).size
            if not pos:
                if inds['crossover'] > 0:
                    self.buy(data=d, size=10)
            if pos > 0:
                if inds['crossover'] < 0:
                    self.close(data=d)