import helpers.Logger as Logger
import Backtest
from Backtest6040Benchmark import Backtest6040Benchmark as Benchmark


def main():
    logger = Logger.Logger()
    logger.Warning("Starting PSRTrade")
    # backtest = Backtest.Backtest()
    # backtest.test()
    Benchmark().test()


if __name__ == '__main__':
    main()
