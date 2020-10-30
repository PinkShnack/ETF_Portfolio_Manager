import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

from download_csv_from_link import get_urls_from_ticker_list, download_urls

class ETF():

    def __init__(self, ticker, etf_name='', dummy_data=False):
        '''
        ETF class allows users to interact with single ETFs, and can be
        imagined as a subset of the Portfolio class.
        Use the Portfolio class to view data from several ETFs.

        Parameters
        ----------

        Attributes
        ----------

        Examples
        --------
        >>> from portfolio.etf import ETF
        >>> ticker = 'CSPX'
        >>> SP500 = ETF(ticker='CSPX', etf_name="S&P 500")
        >>> SP500
        <Portfolio, Cool Portfolio, {'CSPX': 50, 'IAEA': 25, 'SUWU': 25}>

        >>> my_portfolio.df_list[0].head(3)
        '''

        self.ticker = ticker
        self.etf_name = etf_name
        self._load_ticker_init(ticker, dummy_data)


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
