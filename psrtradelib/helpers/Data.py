import tda
import httpx
import json
import datetime
import csv
import io
import pandas as pd
import config
import get_all_tickers
import time
import re
import pickle as pkl
import atexit
import helpers.Logger as Logger

class SecuritiesData(object):
    def __init__(
            self,
            api_key = None,
            redirect_uri = "https://localhost",
            client = None,
            symbol = "AAPL"
        ):
        self.logger = Logger.Logger()
        configModel = config.config()
        self.api_key = api_key or configModel.ameritrade_api_key
        self.redirect_uri = redirect_uri
        self.token_path = './token.pickle'
        self.client = client
        self.symbol = symbol

    def get_client(self):
        try:
            c = tda.auth.client_from_token_file(self.token_path, self.api_key)
        except FileNotFoundError:
            from selenium import webdriver
            from webdriver_manager.chrome import ChromeDriverManager
            with webdriver.Chrome(ChromeDriverManager().install()) as driver:
                c = tda.auth.client_from_login_flow(
                    driver, self.api_key, self.redirect_uri, self.token_path)
        return c

    def get_data(self):
        client = self.get_client()
        r = client.get_price_history(self.symbol,
                period=tda.client.Client.PriceHistory.Period.TEN_YEARS,
                period_type=tda.client.Client.PriceHistory.PeriodType.YEAR,
                frequency_type=tda.client.Client.PriceHistory.FrequencyType.DAILY,
                frequency=tda.client.Client.PriceHistory.Frequency.DAILY)
        assert r.status_code == httpx.codes.OK, r.raise_for_status()
        history = r.json()
        return history

    def get_data_csv(self, datas = None):
        if datas is None:
            datas = self.get_data()
        output = io.StringIO()
        writer = csv.writer(output)

        if "candles" in datas:
            datas = datas["candles"]
        
        for data in datas:
            # number of lines processed
            count = 0

            # Write header row
            if count == 0:
                header = data.keys()
                writer.writerow(header)
                count += 1
            
            writer.writerow(data.values())

        return output.getvalue()

    def get_data_df(self, datas = None):
        if datas is None:
            datas = self.get_data()

        if "candles" in datas:
            datas = datas["candles"]

        df = pd.read_json(json.dumps(datas))
        return df

    def get_symbols(self):
        start = 0
        end = 500
        client = self.get_client()

        symbols = get_all_tickers.get_tickers()
        while (start < len(symbols)):
            tickers = symbols[start:end]
            results = client.search_instruments(tickers)
            data = results.json()
            f_name = time.asctime() + '.pkl'
            f_name = "data/" + re.sub('[ :]', '_', f_name)
            with open(f_name, 'wb') as file:
                pkl.dump(data, file)
            start = end
            end += 500
            time.sleep(1)



    # https://github.com/mariostoev/finviz
