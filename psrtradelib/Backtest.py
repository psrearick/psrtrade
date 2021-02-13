import os, sys, argparse
import strategies.GoldenCross as GoldenCross
import strategies.BuyHold as BuyHold
import strategies.ForceIndexImpulse.main as ForceIndexImpulse
from strategies.FastCross import FastCross
import strategies.MediumCross as MediumCross
import helpers.Data as Data
import helpers.Logger as Logger
import helpers.BacktraderUniverse as bt
import screeners.UptrendPullback as UptrendPullback
import helpers.Providers.AlphaVantage as AlphaVantage
import helpers.Providers.TDAmeritrade as TDAmeritrade


class Backtest:
    def __init__(self):
        self.logger = Logger.Logger()
        # self.dataModel = Data.SecuritiesData(TDAmeritrade)
        self.dataModel = Data.SecuritiesData(AlphaVantage)

    def test(self):
        # Dictionary of strategies
        strategies = {
            "fastcross": FastCross,
            "mediumcross": MediumCross.MediumCross,
            "goldencross": GoldenCross.GoldenCross,
            "buyhold": BuyHold.BuyHold,
            "forceindex": ForceIndexImpulse.ForceIndexImpulse
        }

        # get command line input to determine which strategy to use
        parser = argparse.ArgumentParser()
        parser.add_argument('strategy', help="Select a strategy to test", type=str)
        args = parser.parse_args()
        if args.strategy not in strategies:
            self.logger.Error("invalid strategy, must be one of {}".format(", ".join(strategies.keys())))
            sys.exit()
        strategy = args.strategy

        cerebro = bt.Cerebro()

        cerebro.broker.set_cash(100000)

        # Get data
        assets_list = [
            "AAPL",
            # "AMZN",
            # "GOOG",
            # "FB",
            # "SPY",
            # "DIA"
        ]

        # sample = UptrendPullback.Sample()
        # get_universe = getattr(sample, "get_universe", None)
        # if callable(get_universe):
        #     assets_list = get_universe()

        sd = self.dataModel
        for i in range(len(assets_list)):
            symbol = assets_list[i]
            data = sd.get_cerebro_data(symbol)
            cerebro.adddata(data, name=symbol)
            cerebro.resampledata(data, timeframe=bt.TimeFrame.Weeks, name=symbol + "_long")

        # # Add Strategy and Analyzers
        cerebro.addstrategy(strategies[strategy])
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
        cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
        cerebro.addsizer(bt.sizers.SizerFix, stake=20)

        # Run Cerebro
        self.logger.Warning("Starting portfolio value - %.2f" % cerebro.broker.getvalue())
        results = cerebro.run()
        result = results[0]
        analyzers = result.analyzers
        self.logger.Warning("Ending portfolio value - %.2f" % cerebro.broker.getvalue())

        # Log Results
        ta = analyzers.ta.get_analysis()
        print(ta['total']['total'])
        trade_count = ta['total']['closed'] if ta['total']['total'] > 0 else 0
        win_count = ta['won']['total'] if ta['total']['total'] > 0 else 0
        win_percent = round(win_count / trade_count, 2) if ta['total']['total'] > 0 else 0

        self.logger.Log("Sharpe Ratio - Score: {}".format(analyzers.mysharpe.get_analysis()['sharperatio']))
        self.logger.Log("SQN - Trades: {}, Score: {}".format(analyzers.sqn.get_analysis()['trades'],
                                                             analyzers.sqn.get_analysis()['sqn']))
        self.logger.Log("Total Trades: {}".format(trade_count))
        self.logger.Log("Win Percentage: {}".format(str(win_percent * 100) + "%"))
