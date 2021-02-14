import Config
from alpha_vantage.timeseries import TimeSeries
from helpers.Providers.Provider import ProviderModel
import pandas as pd
import numpy as np


class Provider(ProviderModel):
    def __init__(self):
        super().__init__()
        config_model = Config.Config()
        self.api_key = config_model.alpha_vantage_api_key

    # Get Alpha Vantage API Client
    def get_client(self):
        return TimeSeries(key=self.api_key, output_format='pandas')

    # get data for a specific symbol
    # for a small amount of data, set the output_size to compact
    def get_data(self, symbol):
        c = self.get_client()
        return c.get_daily(symbol=symbol, outputsize='full')

    def get_data_df(self, symbol):
        df, metadata = self.get_data(symbol)
        df.index = pd.to_datetime(df.index, format='%Y%m%d')
        df['Date'] = df.index
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Datetime']
        return df[::-1]

    def get_data_adjusted(self, symbol):
        c = self.get_client()
        return c.get_daily_adjusted(symbol=symbol, outputsize="full")

    def get_data_adjusted_df(self, symbol):
        # Get the adjusted data
        data, metadata = self.get_data_adjusted(symbol)

        # Convert the index to datetime.
        data.index = pd.to_datetime(data.index, format='%Y%m%d')

        # Adjust the rest of the data
        data['adj open'] = np.vectorize(self.adjust)(data.index.date, data['4. close'],
                                                     data['5. adjusted close'], data['1. open'])
        data['adj high'] = np.vectorize(self.adjust)(data.index.date, data['4. close'],
                                                     data['5. adjusted close'], data['2. high'])
        data['adj low'] = np.vectorize(self.adjust)(data.index.date, data['4. close'],
                                                    data['5. adjusted close'], data['3. low'])
        data['Date'] = data.index

        # Extract the columns we want to work with and rename them.
        data = data[['adj open', 'adj high', 'adj low', '5. adjusted close', '6. volume', 'Date']]
        data.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Datetime']

        return data[::-1]

    def adjust(self, date, close, adj_close, in_col):
        rounding = 4

        try:
            factor = adj_close / close
            return round(in_col * factor, rounding)
        except ZeroDivisionError:
            print('WARNING: DIRTY DATA >> {} Close: {} | Adj Close {} | in_col: {}'.format(date, close, adj_close,
                                                                                           in_col))
            return 0
