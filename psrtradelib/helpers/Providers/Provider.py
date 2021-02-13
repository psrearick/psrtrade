from datetime import datetime
import backtrader as bt


class ProviderModel:
    def __init__(self, data=None, symbol=None):
        self.data = data
        self.symbol = symbol

    def get_data_df(self, symbol, data=None):
        pass

    # get data for specified symbol as pandas dataframe after saving it as a csv
    def get_data_csv(self, symbol, data=None):
        data = self.get_data_df(symbol, data)
        output = "psrtradelib/data/" + symbol + "_" + datetime.today().strftime('%Y%m%d')
        data.to_csv(output)
        return data

    def get_cerebro_data(self, symbol):
        data = self.get_data_df(symbol)
        backtestdata = BacktraderData(dataname=data)
        return backtestdata


class BacktraderData(bt.feeds.PandasData):
    params = (
        ('nocase', True),
        ('datetime', 'Datetime'),
        ('open', 'Open'),
        ('high', 'High'),
        ('low', 'Low'),
        ('close', 'Close'),
        ('volume', 'Volume'),
        ('openinterest', None),
    )
