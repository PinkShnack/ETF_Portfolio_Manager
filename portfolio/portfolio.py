
import pandas as pd
import matplotlib.pyplot as plt

import portfolio.io as port_io
from portfolio.etf import ETF


class Portfolio:

    def __init__(self, ticker_percent_dict, country, portfolio_name='',
                 dummy_data=False):
        '''
        Portfolio class allows users to interact with the program intuitively

        Parameters
        ----------

        Attributes
        ----------

        Examples
        --------
        >>> from portfolio.portfolio import Portfolio
        >>> ticker_info = {'AYEM': 100}
        >>> my_portfolio = Portfolio(ticker_info, "GER", "Cool Portfolio", dummy_data=True)
        Downloading Portfolio Data

        >>> my_portfolio
        <Portfolio, Cool Portfolio, {'CSPX': 50, 'IAEA': 25, 'SUWU': 25}, UK>

        The df_list attribute is just a list of Pandas dataframes, allowing
        you to use Pandas for any data analysis you wish.

        >>> df = my_portfolio.df_list[0]

        Check out the first 3 lines in the 'CSPX' Pandas dataframe

        >>> _ = df.head(3)

        Look at the individual ETFs within the Portfolio with etf_list

        >>> etf_info = my_portfolio.etf_list

        Plot the Portfolio summary

        >>> ax = my_portfolio.plot_summarised_portfolio(groupby="Sector")

        Plot the summary of each ETF

        >>> axes = my_portfolio.plot_all_summarised_etf(groupby="Sector")

        Load both ETF and Portfolio with the API

        >>> import portfolio.api as pf
        >>> ticker_percent_dict = {'IVV': 10, 'IWM': 75, 'IEFA': 15}
        >>> my_portfolio_2 = pf.Portfolio(ticker_percent_dict, "US")
        Downloading Portfolio Data

        >>> my_portfolio_2
        <Portfolio, Portfolio 2, {'IVV': 10, 'AGG': 75, 'IWF': 15}>

        Get weighting of single companies

        >>> my_portfolio_2.get_company_info(company_name="Apple")
        APPLE INC has a weighting of 1.309 % in this Portfolio.

        '''

        self.country = country.upper()
        self._ticker_percent_dict_init(ticker_percent_dict)
        self.portfolio_name = portfolio_name
        self.dummy_data = dummy_data
        self.df_list = []
        #self._load_tickers_init(self.ticker_percent_dict, self.dummy_data)
        self.etf_list = []
        self._create_etf_objects()

    def _ticker_percent_dict_init(self, ticker_percent_dict):
        if sum(ticker_percent_dict.values()) == 100:
            self.ticker_percent_dict = ticker_percent_dict
        else:
            raise ValueError(
                "Your ticker_percent_dict percentages don't add up to 100%")

    # def _load_tickers_init(self, ticker_percent_dict, dummy_data):
    #     """ Load the chosen tickers."""

    #     chosen_tickers = [i for i in ticker_percent_dict.keys()]

    #     print("Downloading Portfolio Data")
    #     df_list = port_io.load_tickers(ticker_list=chosen_tickers,
    #                                    dummy_data=dummy_data)

    #     self.df_list = df_list

    def __repr__(self):
        return '<%s, %s, %s, %s>' % (
            self.__class__.__name__,
            self.portfolio_name,
            self.ticker_percent_dict,
            self.country
        )

    def _create_etf_objects(self):

        if not isinstance(self.ticker_percent_dict, dict):
            raise ValueError("ticker_percent_dict must be a dictionary")
        ticker_list = [i for i in self.ticker_percent_dict.keys()]

        print("Downloading Portfolio Data")

        etf_list = []
        df_list = []
        for ticker in ticker_list:
            etf = ETF(ticker, self.country, self.dummy_data)
            etf_list.append(etf)
            df_list.append(etf.df)

        self.etf_list = etf_list
        self.df_list = df_list

    def summarise_portfolio(self, groupby, sort_values_by="Weight (%)"):

        df_weighted_percent_list = []
        for etf in self.etf_list:
            df_grouped = etf.summarise(groupby=groupby,
                                       sort_values_by=sort_values_by)
            percent_to_scale = self.ticker_percent_dict[etf.ticker]/100
            df_grouped[sort_values_by] = df_grouped[sort_values_by].mul(
                percent_to_scale)
            df_weighted_percent_list.append(df_grouped)

        df_all_grouped = pd.DataFrame()
        for df_weighted in df_weighted_percent_list:
            df_all_grouped = pd.concat(
                [df_all_grouped, df_weighted], ignore_index=True)

        df_portfolio_summarised = df_all_grouped.groupby(
            [groupby], as_index=False).sum().sort_values(
                by=sort_values_by, ascending=False, ignore_index=True)

        df_portfolio_summarised[sort_values_by].sum()

        return df_portfolio_summarised

    def plot_summarised_portfolio(self, groupby, sort_values_by="Weight (%)",
                                  kind="barh", legend=False, figsize=(10, 16),
                                  fontsize=24, save=False, **kwargs):

        df_portfolio_summarised = self.summarise_portfolio(
            groupby=groupby, sort_values_by=sort_values_by)

        ax = df_portfolio_summarised.plot(x=groupby, y=sort_values_by,
                                          kind=kind, legend=legend,
                                          figsize=figsize, **kwargs)
        plt.title(f"Portfolio {groupby}", fontsize=fontsize)
        plt.xlabel("Percentage", fontsize=fontsize)
        plt.ylabel(groupby, fontsize=fontsize)
        plt.xticks(fontsize=fontsize-4)
        plt.yticks(fontsize=fontsize-4)
        plt.tight_layout()
        if save:
            plt.savefig(f"Portfolio {groupby}.png")

        return ax

    def plot_all_summarised_etf(self, groupby, sort_values_by="Weight (%)",
                                kind="barh", legend=False, save=False,
                                **kwargs):
        ax_list = []
        for etf in self.etf_list:
            ax = etf.plot_summarised_etf(
                groupby=groupby, sort_values_by=sort_values_by, kind=kind,
                legend=legend, save=save, **kwargs)
            ax_list.append(ax)

        return ax_list

    def get_company_info(self, company_name, sort_values_by="Weight (%)"):

        company_etf_weight = 0
        for etf in self.etf_list:
            fn, company_weight = etf._company_weighting(
                company_name, sort_values_by)

            if company_weight is not None:
                percent_to_scale = self.ticker_percent_dict[etf.ticker]/100

                company_etf_weight += company_weight * percent_to_scale

                full_name = fn

        print(f"{full_name} has a weighting of {company_etf_weight:.3f} % "
              "in this Portfolio.")
