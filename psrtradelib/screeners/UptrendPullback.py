from finviz.screener import Screener
import helpers.Logger as Logger

class Sample():
    def __init__(self):
        self.logger = Logger.Logger()

    def get_universe(self):
        # Asset Type: EQUITY
        # Market Cap: Over 2 Billion
        # Country: USA
        # Sector: "Consumer Cyclical", "Technology", "Communication Services"
        # Average Volume: Over 1 Million
        # Beta: Over 1
        filters = [
            'cap_midover',
            'geo_usa',
            'sec_communicationservices|consumercyclical|technology',
            'sh_avgvol_o1000',
            'ta_beta_o1'
        ]
        
        return Screener(filters=filters, table='Performance', order='price')
    
    def get_tickers(self):
        stock_list = self.get_universe()
        tickers = []

        for stock in stock_list:
            tickers.append(stock['Ticker'])
        
        return tickers
            