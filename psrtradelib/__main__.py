import helpers.Logger as Logger
from Backtest import Backtest
from Backtest6040Benchmark import Backtest6040Benchmark as Benchmark


def main():
    logger = Logger.Logger()
    logger.Warning("Starting PSRTrade")
    Backtest().test()
    # Benchmark().test()


if __name__ == '__main__':
    main()
