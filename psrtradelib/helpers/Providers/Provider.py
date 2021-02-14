from datetime import datetime
import backtrader as bt
import pandas as pd
import glob
import re
import os


class ProviderModel:
    def __init__(self, data=None, symbol=None):
        self.data = data
        self.symbol = symbol

    def get_data_df_from_csv(self, symbol):
        # define filename pattern and get path
        path = "psrtradelib/data"
        filename = glob.glob("{}/{}_*.csv".format(path, symbol))

        # If the file exists, get its date from its name
        date = None
        if len(filename) > 0:
            filename = filename[0]
            m = re.search("{}/{}_(.+?).csv".format(path, symbol), filename)
            if m:
                date = m.group(1)

        # If a date is not found, return
        if date is None:
            return self.get_data_csv(symbol)

        # Determine if the data is more than a month old
        # if not, return the data
        data = pd.read_csv(filename, parse_dates=['date', 'Datetime'])
        now = datetime.now()
        saved = datetime.strptime(date, '%Y%m%d')
        if (now - saved).days < 31:
            return data

        # Replace old file with new data
        os.remove(filename)
        new_filename = "{}/{}_{}.csv".format(path, symbol, now.strftime('%Y%m%d'))
        df = self.get_data_df(symbol)
        df.to_csv(new_filename)

        return data

    def get_data_df(self, symbol, data=None):
        pass

    # get data for specified symbol as pandas dataframe after saving it as a csv
    def get_data_csv(self, symbol, data=None):
        data = self.get_data_df(symbol, data)
        output = "psrtradelib/data/" + symbol + "_" + datetime.today().strftime('%Y%m%d') + ".csv"
        data.to_csv(output)
        return data

    def get_cerebro_data(self, symbol):
        data = self.get_data_df(symbol)
        return BacktraderData(dataname=data)

    def get_cerebro_data_from_csv(self, symbol):
        data = self.get_data_df_from_csv(symbol)
        return BacktraderData(dataname=data)


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
