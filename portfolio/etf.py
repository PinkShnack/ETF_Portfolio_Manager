import pandas as pd
import matplotlib.pyplot as plt

import portfolio.io as port_io
import portfolio.setup_data as setup_data


class ETF():

    def __init__(self, ticker, dummy_data=False):
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
        >>> SP500 = ETF(ticker='CSPX')
        >>> SP500
        <ETF, CSPX, iShares Core S&P 500 UCITS ETF USD (Acc)>

        The df attribute is just a Pandas dataframe, allowing you to use Pandas
        for any data analysis you wish.

        >>> df = SP500.df

        Check out the first 3 lines in the Pandas dataframe

        >>> _ = SP500.df.head(3)
        >>> SP500.plot_summarised_ETF(groupby="Sector")

        '''

        self.ticker = ticker
        self._etf_ticker_name_init()
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

    def _etf_ticker_name_init(self):
        info = setup_data.get_info_using_ticker_list([self.ticker], 'name')
        self.etf_name = info[0]

    def summarise(self, groupby, sort_values_by="Weight (%)"):

        df_grouped = self.df.groupby([groupby.capitalize()],
                     as_index=False).sum().sort_values(
                         by=sort_values_by, ascending=False, ignore_index=True)

        return df_grouped
    
    def plot_summarised_ETF(
            self, groupby, sort_values_by="Weight (%)", kind="barh",
            legend=False, save=False, **kwargs):

        df_grouped = self.summarise(groupby=groupby)

        ax = df_grouped.plot(x=groupby, y=sort_values_by,
                             kind=kind, legend=legend, **kwargs)

        plt.title(self.etf_name)
        plt.tight_layout()
        if save:
            plt.savefig(f"{self.ticker}_{groupby}.png")
        
        return ax

