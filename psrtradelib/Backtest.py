import os, sys, argparse
import strategies.GoldenCross as GoldenCross
import strategies.BuyHold as BuyHold
import strategies.ForceIndexImpulse.main as ForceIndexImpulse
import helpers.Data
import helpers.Logger
import helpers.BacktraderUniverse as bt

class Backtest():
    def __init__(self):
        self.logger = helpers.Logger.Logger()
        self.dataModel = helpers.Data.SecuritiesData

    def test(self):
        # Dictionary of strategies
        strategies = {
            "goldencross": GoldenCross.GoldenCross,
            "buyhold": BuyHold.BuyHold,
            "forceindex": ForceIndexImpulse.ForceIndexImpulse
        }

        # get command line input to determine which strategy to use
        parser = argparse.ArgumentParser()
        parser.add_argument('strategy', help="Select a strategy to test", type=str)
        args = parser.parse_args()
        if not args.strategy in strategies:
            self.logger.Error("invalid strategy, must be one of {}".format(", ".join(strategies.keys())))
            sys.exit()
        strategy = args.strategy

        cerebro = bt.Cerebro()

        cerebro.broker.set_cash(100000)

        # Get data
        sd = self.dataModel()
        data = bt.feeds.PandasData(
            dataname=sd.get_data_df(),
            datetime = 5,
            open = 0,
            high = 1,
            low = 2,
            close = 3,
            volume = 4
            )

        # Add daily and weekly data
        cerebro.adddata(data)
        cerebro.resampledata(data, timeframe=bt.TimeFrame.Weeks)

        cerebro.addstrategy(strategies[strategy])

        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
        cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")
        # cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")

        # cerebro.addsizer(bt.sizers.FixedSize, stake=100)

        self.logger.Warning("Starting portfolio value - %.2f" % cerebro.broker.getvalue())

        results = cerebro.run()
        result = results[0]
        analyzers = result.analyzers

        self.logger.Warning("Ending portfolio value - %.2f" % cerebro.broker.getvalue())

        self.logger.Log("Sharpe Ratio - Score: {}".format(analyzers.mysharpe.get_analysis()['sharperatio']))
        self.logger.Log("SQN - Trades: {}, Score: {}".format(analyzers.sqn.get_analysis()['trades'], analyzers.sqn.get_analysis()['sqn']))
        # print("Total Trades: {}".format(thestrat.analyzers.ta.get_analysis()['total']['closed']))
        # print("Total Wins: {}".format(thestrat.analyzers.ta.get_analysis()['won']['total']))
        # print("Total Losses: {}".format(thestrat.analyzers.ta.get_analysis()['lost']['total']))

        # cerebro.plot()