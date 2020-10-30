import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

from portfolio.download_csv_from_link import (get_urls_from_ticker_list,
    download_urls)

class Portfolio():

    def __init__(self, ticker_percent_dict, portfolio_name='', dummy_data=False):
        '''
        Portfolio class allows users to interact with the program intuitively

        Parameters
        ----------

        Attributes
        ----------

        Examples
        --------
        >>> from portfolio import Portfolio
        >>> ticker_percent_dict = {'CSPX': 50, 'IAEA': 25, 'SUWU': 25}
        >>> my_portfolio = Portfolio(ticker_percent_dict, "Cool Portfolio")
        >>> my_portfolio
        <Portfolio, Cool Portfolio, {'CSPX': 50, 'IAEA': 25, 'SUWU': 25}>

        >>> my_portfolio.df_list[0].head(3)
        '''

        self._ticker_percent_dict_init(ticker_percent_dict)
        self.portfolio_name = portfolio_name
        self.df_list = []
        self._load_tickers_init(ticker_percent_dict, dummy_data)


    def _ticker_percent_dict_init(self, ticker_percent_dict):
        if sum(ticker_percent_dict.values()) == 100:
            self.ticker_percent_dict = ticker_percent_dict
        else:
            raise ValueError(
                "Your ticker_percent_dict percentages don't add up to 100%")


    def _load_tickers_init(self, ticker_percent_dict, dummy_data=False):

        """ Load the chosen tickers."""

        if not isinstance(ticker_percent_dict, dict):
            raise ValueError("ticker_percent_dict must be a dictionary")

        chosen_tickers = [i for i in ticker_percent_dict.keys()]

        if dummy_data:
            print("Grabbing Dummy Data")
            fnames = glob("dummy_data/*.csv")
            filenames = []
            for csv_file in fnames:
                for ticker in chosen_tickers:
                    if ticker in csv_file:
                        filenames.append(csv_file)
            
            df_list = []
            for filename in filenames:
                df_list.append(pd.read_csv(filename, header=2))

        else:
            print("Downloading ETF Data")
            df_list = download_urls(
                get_urls_from_ticker_list(chosen_tickers))

        self.df_list = df_list
        
    def __repr__(self):
        return '<%s, %s, %s>' % (
            self.__class__.__name__,
            self.portfolio_name,
            self.ticker_percent_dict
        )
