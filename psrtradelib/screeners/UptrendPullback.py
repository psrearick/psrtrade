from finviz.screener import Screener

class Sample():

    def get_stock_list():
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
        
        stock_list = Screener(filters=filters, table='Performance', order='price')

        for stock in stock_list:  # Loop through 10th - 20th stocks
            print(stock['Ticker'], stock['Price']) # Print symbol and price