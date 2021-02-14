import backtrader as bt
from datetime import datetime
import helpers.Logger as Logger
from strategies.Rebalance import Rebalance
import helpers.Data as Data
import helpers.Providers.AlphaVantage as AlphaVantage


class Backtest6040Benchmark:
    def __init__(self):
        self.logger = Logger.Logger()
        # self.dataModel = Data.SecuritiesData(TDAmeritrade)
        self.dataModel = Data.SecuritiesData(AlphaVantage)

    def test(self):
        # Create an instance of cerebro
        cerebro = bt.Cerebro()

        # Set our desired cash start
        start_cash = 10000
        cerebro.broker.setcash(start_cash)
        cerebro.broker.set_checksubmit(False)

        # strategy Params
        assets_list = [
            ('SPY', 60),
            ('AGG', 40)
        ]

        # Add Data
        symbol_list = [x[0] for x in assets_list]
        sd = self.dataModel
        for i in range(len(assets_list)):
            symbol = assets_list[i][0]
            data = sd.get_cerebro_data_from_csv(symbol, adjusted=True)
            cerebro.adddata(data, name=symbol)

        # Add our strategy
        cerebro.addstrategy(Rebalance, assets=assets_list)

        cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")

        # Run over everything
        results = cerebro.run()
        analyzers = results[0].analyzers

        # Get final portfolio Value
        portfolio_value = cerebro.broker.getvalue()
        pnl = portfolio_value - start_cash

        # Print out the final result
        self.logger.Log('Final Portfolio Value: ${}'.format(portfolio_value))
        self.logger.Log('P/L: ${}'.format(pnl))
        returns = analyzers.returns.get_analysis()
        self.logger.Warning(returns['rnorm100'])

        # Finally plot the end results

        cerebro.plot(style='candlestick')
