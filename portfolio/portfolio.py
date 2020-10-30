
import portfolio.io as port_io
from portfolio.etf import ETF
import portfolio.setup_data as setup_data


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
        >>> from portfolio.portfolio import Portfolio
        >>> ticker_percent_dict = {'CSPX': 50, 'IAEA': 25, 'SUWU': 25}
        >>> my_portfolio = Portfolio(ticker_percent_dict, "Cool Portfolio")
        Downloading Portfolio Data

        >>> my_portfolio
        <Portfolio, Cool Portfolio, {'CSPX': 50, 'IAEA': 25, 'SUWU': 25}>

        The df_list attribute is just a list of Pandas dataframes, allowing
        you to use Pandas for any data analysis you wish.

        >>> df = my_portfolio.df_list[0]

        Check out the first 3 lines in the 'CSPX' Pandas dataframe

        >>> _ = df.head(3)

        Look at the individual ETFs within the Portfolio with etf_list

        >>> etf_info = my_portfolio.etf_list

        Load both ETF and Portfolio with the API

        >>> import portfolio.api as pf
        >>> ticker_percent_dict = {'CSPX': 10, 'IAEA': 75, 'SUWU': 15}
        >>> my_portfolio_2 = pf.Portfolio(ticker_percent_dict, "Portfolio 2")
        Downloading Portfolio Data

        >>> my_portfolio_2
        <Portfolio, Portfolio 2, {'CSPX': 10, 'IAEA': 75, 'SUWU': 15}>

        '''

        self._ticker_percent_dict_init(ticker_percent_dict)
        self.portfolio_name = portfolio_name
        self.dummy_data = dummy_data
        self.df_list = []
        self._load_tickers_init(self.ticker_percent_dict, self.dummy_data)
        self.etf_list = []
        self._create_etf_objects(self.ticker_percent_dict)

    def _ticker_percent_dict_init(self, ticker_percent_dict):
        if sum(ticker_percent_dict.values()) == 100:
            self.ticker_percent_dict = ticker_percent_dict
        else:
            raise ValueError(
                "Your ticker_percent_dict percentages don't add up to 100%")

    def _load_tickers_init(self, ticker_percent_dict, dummy_data):
        """ Load the chosen tickers."""

        if not isinstance(ticker_percent_dict, dict):
            raise ValueError("ticker_percent_dict must be a dictionary")

        chosen_tickers = [i for i in ticker_percent_dict.keys()]

        print("Downloading Portfolio Data")
        df_list = port_io.load_tickers(ticker_list=chosen_tickers,
                                       dummy_data=dummy_data)

        self.df_list = df_list

    def __repr__(self):
        return '<%s, %s, %s>' % (
            self.__class__.__name__,
            self.portfolio_name,
            self.ticker_percent_dict
        )

    def _create_etf_objects(self, ticker_percent_dict):

        ticker_list = [i for i in self.ticker_percent_dict.keys()]

        info = setup_data.get_info_using_ticker_list(ticker_list, 'name')

        etf_list = []
        for ticker, info_ in zip(ticker_list, info):
            etf_list.append(ETF(ticker=ticker, etf_name=info_))

        self.etf_list = etf_list
