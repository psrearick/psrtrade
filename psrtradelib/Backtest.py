import os, sys, argparse
import strategies.BuyHold as BuyHold
import strategies.ForceIndexImpulse.main as ForceIndexImpulse
from strategies.MACross import MACross
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
            "fastcross": [MACross, {'fast': 5, 'slow': 20}],
            "mediumcross": [MACross, {'fast': 20, 'slow': 50}],
            "goldencross": [MACross, {'fast': 50, 'slow': 200}],
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

        cerebro.broker.set_cash(10000)

        # Get data
        assets_list = [
            "AAPL",
            "AMZN",
            "GOOG",
            "FB",
            "SPY",
            "DIA"
        ]

        # assets_list = [
        #     "SPY",
        #     "AGG"
        # ]

        # sample = UptrendPullback.Sample()
        # get_universe = getattr(sample, "get_universe", None)
        # if callable(get_universe):
        #     assets_list = get_universe()

        sd = self.dataModel
        for i in range(len(assets_list)):
            symbol = assets_list[i]
            data = sd.get_cerebro_data_from_csv(symbol)
            cerebro.adddata(data, name=symbol)
            cerebro.resampledata(data, timeframe=bt.TimeFrame.Weeks, name=symbol + "_long")

        # # Add Strategy, Sizer, and Analyzers
        cerebro.addstrategy(strategies[strategy][0], **strategies[strategy][1])
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
        cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
        cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")
        # cerebro.addsizer(bt.sizers.SizerFix, stake=20)

        # Run Cerebro
        self.logger.Log("Starting portfolio value - %.2f" % cerebro.broker.getvalue())
        results = cerebro.run()
        result = results[0]
        analyzers = result.analyzers
        self.logger.Log("Ending portfolio value - %.2f" % cerebro.broker.getvalue())

        # Log Results
        returns = analyzers.returns.get_analysis()
        self.logger.Warning(returns['rnorm100'])
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

        cerebro.plot()
