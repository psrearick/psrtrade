import math
import backtrader as bt
import numpy as np

class ForceIndexImpulse(bt.Strategy):

    def __init__(self):
        self.buy_order = None
        self.stop_loss = 0
        self.profit = 0
        self.order = None
        self.fast = 13
        self.slow = 26
        self.trend_fast = 50
        self.trend_slow = 200
        self.atr_multiplier = 2
        self.order_percentage = 0.95
        self.size = 0

        self.atr = bt.indicators.ATR(period=self.slow)
        self.sma_fast = bt.indicators.SMA(self.data.close, period=self.trend_fast)
        self.sma_slow = bt.indicators.SMA(self.data.close, period=self.trend_slow)
        self.macdHisto = bt.indicators.MACDHisto(self.data.close)
        self.macdHisto1 = bt.indicators.MACDHisto(self.data1.close)
        self.ema_fast = bt.indicators.EMA(self.data.close, period=self.fast)
        self.ema_slow = bt.indicators.EMA(self.data.close, period=self.slow)
        self.ema_long_fast = bt.indicators.EMA(self.data1.close, period=self.fast)
        self.ema_low = bt.indicators.EMA(self.data.low, period=self.fast)
        self.force_index_short_fast = GenericEMA(2)
        self.force_index_short_slow = GenericEMA(13)
        self.force_index_long_slow = GenericEMA(13)


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                pass
                # print(
                #     'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                #     (order.executed.price,
                #      order.executed.value,
                #      order.executed.comm))

            else:  # Sell
                self.stop_loss = 0
                self.profit = 0
                # print('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                #          (order.executed.price,
                #           order.executed.value,
                #           order.executed.comm))

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            pass
            # print('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def next(self):
        day = self.data
        week = self.data1
        

        if self.position.size == 0 and not self.order:
            # ======================================== #
            # --- Upward Trending                  --- #
            # ======================================== #
            if self.sma_fast[0] < self.sma_slow[0]: return

            # ======================================== #
            # --- Elder Impulse System             --- #
            # ======================================== #
            # Impulse System must not be prohibitive
            impulse = self.get_impulse(self.macdHisto.histo, self.ema_fast)
            impulseLong = self.get_impulse(self.macdHisto1.histo, self.ema_long_fast)
            if impulse < 0: return
            if impulseLong < 0: return

            # ======================================== #
            # --- Elder Force Index                --- #
            # ======================================== #
            # Force index EMA must be down on the daily and up on the weekly and slow daily
            self.force_index_short_fast.Update(self.get_force_index(day))
            self.force_index_short_slow.Update(self.get_force_index(day))
            self.force_index_long_slow.Update(self.get_force_index(week))
            if (self.force_index_short_fast.Value or 0) > 0: return
            # if (self.force_index_short_slow.Value or 0) < 0: return
            if (self.force_index_long_slow.Value or 0) < 0: return

            # ======================================== #
            # --- Value Zone                       --- #
            # ======================================== #
            # Close must be in the value zone, below fast EMA and above slow EMA
            if self.ema_fast[0] < self.ema_slow[0]: return
            if day.close[0] > self.ema_fast[0]: return
            # if day.close[0] < self.ema_slow[0]: return

            # ======================================== #
            # --- Calcluate Buy Price              --- #
            # ======================================== #
            estimated_ema = (self.ema_fast[0] * 2) - self.ema_fast[-1]
            limit = (estimated_ema * 2) - self.ema_low[0]
            buy_price = limit if self.ema_slow[0] < limit else self.ema_slow[0]

            # ======================================== #
            # --- Enter Limit Order                --- #
            # ======================================== #
            amount_to_invest = (self.order_percentage * self.broker.cash)
            self.size = math.floor(amount_to_invest / self.data.close)
            print("{}: Buy {} shares at {}".format(self.data.datetime.date(), self.size, day.close[0]))
            # self.order = self.buy(exectype=bt.Order.Limit, price=buy_price, size=self.size)

        if self.position.size > 0:
            self.calculate_close()
            # print([self.profit, close, self.stop_loss])
            if day.close[0] > self.profit or day.close[0] < self.stop_loss:
                # print("{}: Sell at {}".format(self.data.datetime.date(), day.close[0]))
                self.close()

    def calculate_close(self):
        self.calculate_stop_loss()
        self.calculate_take_profit()

    def calculate_stop_loss(self):
        max_drawdown = self.atr[0] * self.atr_multiplier
        stop = self.data.close[0] - max_drawdown
        if stop > self.stop_loss: self.stop_loss = stop

    def calculate_take_profit(self):
        self.profit = self.ema_fast[0] + (2 * self.atr[0])

    def get_impulse(self, macd, ma):
        # Calculate value for Elder Impulse System
        if (macd[0] > macd[-1] and ma[0] > ma[-1]):
            return 1
        if macd[0] < macd[-1] and ma[0] < ma[-1]:
            return -1
        return 0

    def get_force_index(self, bar):
        return (bar.close[0] - bar.close[-1]) * bar.volume

class GenericEMA():
    def __init__(self, length, smoothing=2):
        self.Value = None
        self.Period = length
        self.Length = length + 1
        self.Smoothing = smoothing
        self.Multiplier = self.Smoothing / self.Length
        self.History = []

    def Update(self, val):
        self.History.append(val)
        count = len(self.History)
        if count < self.Period: return True
        if count == self.Period:
            self.Value = sum(self.History) / count
            return True
        if count > self.Length:
            self.History.pop(0)
        self.Value = (val * self.Multiplier) + (self.Value * (1 - self.Multiplier))
        return True