import helpers.Logger as Logger


class SecuritiesData(object):
    def __init__(self, provider):
        self.logger = Logger.Logger()
        self.provider = provider.Provider()

    # get provider client
    def get_client(self):
        return self.provider.get_client()

    def get_data_df_from_csv(self, symbol):
        return self.provider.get_data_df_from_csv(symbol)

    # Using client, get data for specified symbol using clients default return format
    def get_data(self, symbol):
        return self.provider.get_data(symbol)

    # get data for specified symbol as pandas dataframe
    def get_data_df(self, symbol, data=None):
        return self.provider.get_data_csv(symbol, data)

    # get data for specified symbol as pandas dataframe after saving it as a csv
    def get_data_csv(self, symbol, data=None):
        return self.provider.get_data_csv(symbol, data)

    def get_cerebro_data(self, symbol):
        return self.provider.get_cerebro_data(symbol)

    def get_cerebro_data_from_csv(self, symbol, adjusted=False):
        return self.provider.get_cerebro_data_from_csv(symbol, adjusted)
