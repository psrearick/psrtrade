import Config
from alpha_vantage.timeseries import TimeSeries
from helpers.Providers.Provider import ProviderModel
import pandas as pd


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
    def get_data(self, symbol, output_size='full'):
        c = self.get_client()
        return c.get_daily(symbol=symbol, outputsize=output_size)

    def get_data_df(self, symbol, output_size='full'):
        df, metadata = self.get_data(symbol, output_size)
        df.index = pd.to_datetime(df.index, format='%Y%m%d')
        df['Date'] = df.index
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Datetime']
        return df[::-1]
