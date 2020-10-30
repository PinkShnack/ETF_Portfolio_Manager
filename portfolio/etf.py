import pandas as pd
import matplotlib.pyplot as plt

import portfolio.io as port_io


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
        <ETF, S&P 500, CSPX>

        The df attribute is just a Pandas dataframe, allowing you to use Pandas
        for any data analysis you wish.

        >>> df = SP500.df

        Check out the first 3 lines in the Pandas dataframe

        >>> _ = SP500.df.head(3)

        '''

        self.ticker = ticker
        self.etf_name = etf_name
        self.df = None  # will be replaced with df when loaded
        self.dummy_data = dummy_data
        self._load_tickers_init(self.ticker, self.dummy_data)

    def _load_tickers_init(self, ticker, dummy_data):
        """ Load the chosen ticker."""

        if not isinstance(ticker, str):
            raise ValueError("ticker must be a string")

        df_list = port_io.load_tickers(ticker_list=[ticker],
                                       dummy_data=dummy_data)

        if len(df_list) != 1:
            raise ValueError("Problem with loading ETF, should be just 1 "
                             "ticker, but more than 1 loaded")
        else:
            df = df_list[0]

        self.df = df

    def __repr__(self):
        return '<%s, %s, %s>' % (
            self.__class__.__name__,
            self.ticker,
            self.etf_name
        )
