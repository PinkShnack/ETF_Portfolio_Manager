import pandas as pd

from portfolio.etf import ETF


def test_etf_creation():
    ticker = "CSPX"
    country = "UK"
    etf1 = ETF(ticker, country)
    assert isinstance(etf1, ETF)
    assert isinstance(etf1.df, pd.DataFrame)

    assert isinstance(etf1.ticker, str)
    assert etf1.ticker == ticker

    assert isinstance(etf1.country, str)
    assert etf1.country == country

    assert isinstance(etf1.default_sort_values_by, str)
    assert etf1.default_sort_values_by == "Weight (%)"

    assert isinstance(etf1.dummy_data, bool)
    assert not etf1.dummy_data


def test_etf_country():
    ticker = "CSPX"
    country = "uk"
    etf1 = ETF(ticker, country)
    # The country code is made uppercase
    assert etf1.country == "UK"


def test_etf_summarise1():
    ticker = "CSPX"
    country = "uk"
    etf1 = ETF(ticker, country)
    grpd = etf1.summarise("Sector")
    assert isinstance(grpd, pd.DataFrame)
