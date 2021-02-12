import helpers.Logger
import Backtest

def main():
    logger = helpers.Logger.Logger()
    backtest = Backtest.Backtest()
    logger.Warning("Starting PSRTrade")
    backtest.test()


if __name__ == '__main__':
    main()
