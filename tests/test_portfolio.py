import pandas as pd

from portfolio.portfolio import Portfolio
from portfolio.etf import ETF


def test_etf_creation():
    ticker_info = {'CSPX': 100}
    country = "UK"
    pf1 = Portfolio(ticker_info, country)
    assert isinstance(pf1, Portfolio)

    assert isinstance(pf1.etf_list, list)
    assert isinstance(pf1.etf_list[0], ETF)

    assert isinstance(pf1.df_list, list)
    assert isinstance(pf1.df_list[0], pd.DataFrame)

    assert isinstance(pf1.ticker_percent_dict, dict)
    assert pf1.ticker_percent_dict == ticker_info

    assert isinstance(pf1.country, str)
    assert pf1.country == country

    assert isinstance(pf1.portfolio_name, str)
    assert pf1.portfolio_name == ""

    assert isinstance(pf1.dummy_data, bool)
    assert not pf1.dummy_data
