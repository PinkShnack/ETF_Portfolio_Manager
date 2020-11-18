
import matplotlib.pyplot as plt

import portfolio.io as port_io
import portfolio.setup_data as setup_data


class ETF():

    def __init__(self, ticker, country, dummy_data=False):
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
        >>> SP500 = ETF(ticker='CSPX', country="UK")
        >>> SP500
        <ETF, CSPX, iShares Core S&P 500 UCITS ETF USD (Acc)>

        The df attribute is just a Pandas dataframe, allowing you to use Pandas
        for any data analysis you wish.

        >>> df = SP500.df

        Check out the first 3 lines in the Pandas dataframe

        >>> _ = SP500.df.head(3)
        >>> ax = SP500.plot_summarised_etf(groupby="Sector")

        Look at the weighting of a single company

        >>> SP500.get_company_info(company_name="Apple")
        APPLE INC has a weighting of 6.4 % in this ETF.
        ('APPLE INC', 6.4)


        '''

        self.ticker = ticker
        self.country = country.upper()
        self.default_sort_values_by = "Weight (%)"
        self._etf_ticker_name_init()
        self.df = None  # will be replaced with df when loaded
        self.dummy_data = dummy_data
        self._load_tickers_init(self.ticker, self.dummy_data)


    def _load_tickers_init(self, ticker, dummy_data):
        """ Load the chosen ticker."""

        if not isinstance(ticker, str):
            raise ValueError("ticker must be a string")

        df_list = port_io.load_tickers(ticker_list=[ticker],
                                       country=self.country,
                                       dummy_data=self.dummy_data)

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
        info = setup_data.get_info_using_ticker_list(
            [self.ticker], 'name', self.country)
        self.etf_name = info[0]

    def summarise(self, groupby, sort_values_by="auto"):

        if sort_values_by == "auto":
            sort_values_by = self.default_sort_values_by
        df_grouped = self.df.groupby([groupby.capitalize()],
                                     as_index=False).sum().sort_values(
            by=sort_values_by, ascending=False, ignore_index=True)

        return df_grouped

    def plot_summarised_etf(
            self, groupby, sort_values_by="auto", kind="barh",
            legend=False, save=False, **kwargs):

        if sort_values_by == "auto":
            sort_values_by = self.default_sort_values_by

        df_grouped = self.summarise(groupby=groupby)

        ax = df_grouped.plot(x=groupby, y=sort_values_by,
                             kind=kind, legend=legend, **kwargs)

        plt.title(self.etf_name)
        plt.tight_layout()
        if save:
            plt.savefig(f"{self.ticker}_{groupby}.png")

        return ax

    def get_company_info(self, company_name, sort_values_by="auto"):

        if sort_values_by == "auto":
            sort_values_by = self.default_sort_values_by

        full_name, company_weight = self._company_weighting(
            company_name, sort_values_by)

        print(f"{full_name} has a weighting of {company_weight} % "
              "in this ETF.")

        return(full_name, company_weight)

    def _company_weighting(self, company_name, sort_values_by="auto"):

        if sort_values_by == "auto":
            sort_values_by = self.default_sort_values_by

        df_copy = self.df.copy()

        # Make the company name the index so we can filter by it
        df_copy.drop(df_copy.tail(1).index, inplace=True)
        df_copy.set_index("Name", inplace=True)

        # find the company name in the new name index
        full_name = []
        for index_name in df_copy.index:
            if company_name.upper() in index_name.upper():
                full_name.append(index_name)

        # check if there is only one matching name
        if len(full_name) == 1:
            full_name = full_name[0]
            company_weight = df_copy.at[full_name, sort_values_by]
            return(full_name, company_weight)
        elif len(full_name) > 1:
            raise ValueError("More than one company found, maybe the name you "
                             "gave was ambiguous.")
        else:
            return('', None)
