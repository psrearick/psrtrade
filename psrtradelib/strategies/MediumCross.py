import math
import backtrader as bt

class MediumCross(bt.Strategy):

    params = (
        ('fast', 20),
        ('slow', 50),
        ("order_percentage", 0.95),
        ("ticker", "SPY")
    )

    def __init__(self):
        self.fast_moving_average = bt.indicators.SMA(
            self.data.close, period=self.p.fast, plotname='20-Day` SMA'
        )

        self.slow_moving_average = bt.indicators.SMA(
            self.data.close, period=self.p.slow, plotname='50-Day SMA'
        )

        self.crossover = bt.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average)

    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                amount_to_invest = (self.p.order_percentage * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)

                # print("Buy {} Shares of {} at {}".format(self.size, self.p.ticker, self.data.close[0]))
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.crossover < 0:
                # print("Sell {} Shares of {} at {}".format(self.size, self.p.ticker, self.data.close[0]))
                self.close()