import tda
import Config
import httpx
import json
from datetime import datetime
import pandas as pd
from helpers.Providers.Provider import ProviderModel


class Provider(ProviderModel):
    def __init__(self):
        super(Provider, self).__init__()
        config_model = Config.Config()
        self.api_key = config_model.ameritrade_api_key

    # Get TDAmeritrade API Client
    def get_client(self):
        token_path = './token.pickle'
        redirect_uri = 'https://localhost'
        try:
            c = tda.auth.client_from_token_file(token_path, self.api_key)
        except FileNotFoundError:
            from selenium import webdriver
            from webdriver_manager.chrome import ChromeDriverManager
            with webdriver.Chrome(ChromeDriverManager().install()) as driver:
                c = tda.auth.client_from_login_flow(
                    driver, self.api_key, redirect_uri, token_path)
        return c

    # Using client, get data for specified symbol
    def get_data(self, symbol):
        client = self.get_client()
        r = client.get_price_history(symbol,
                                     period=tda.client.Client.PriceHistory.Period.TEN_YEARS,
                                     period_type=tda.client.Client.PriceHistory.PeriodType.YEAR,
                                     frequency_type=tda.client.Client.PriceHistory.FrequencyType.DAILY,
                                     frequency=tda.client.Client.PriceHistory.Frequency.DAILY)
        assert r.status_code == httpx.codes.OK, r.raise_for_status()
        history = r.json()
        return history

    # get data for specified symbol as pandas dataframe
    def get_data_df(self, symbol, data=None):
        if data is None:
            data = self.get_data(symbol)

        if "candles" in data:
            data = data["candles"]

        df = pd.read_json(json.dumps(data))
        return df
