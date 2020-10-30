import pandas as pd
import os
from portfolio import setup_data


def get_urls_from_ticker_list(ticker_list):

    """
    Get http link for etfs in ishares website.

    Examples
    --------
    >>> from download_csv_from_link import get_urls_from_ticker_list
    >>> ticker_list = ['CSPX', 'IAEA', 'SUWU']
    >>> url_list = get_urls_from_ticker_list(ticker_list)
    >>> url_list[0]
    'https://www.ishares.com/uk/individual/en/products/253743/*/1506575576011.ajax?fileType=csv&fileName=CSPX_holdings&dataType=fund'

    >>> len(url_list)
    3

    >>> len(ticker_list)
    3

    """

    ticker_code_number_dict = setup_data.create_ticker_code_number_dict()

    chosen_tickers_dict = {}
    for k, v in ticker_code_number_dict.items():
        for ticker in ticker_list:
            if ticker == k:
                chosen_tickers_dict[k] = v

    url_list = []
    for key, val in chosen_tickers_dict.items():
        url_string = f"https://www.ishares.com/uk/individual/en/products/{val}/*/1506575576011.ajax?fileType=csv&fileName={key}_holdings&dataType=fund"
        url_list.append(url_string)

    if len(ticker_list) != len(url_list):
        raise ValueError(
            "Ticker list and URL list not the same length. This "
            "means that one or more ETF datasets were not found. This is "
            "likely due to the tickers not being applicable to the country you"
            " have chosen.")

    return(url_list)


def download_urls(url_list):

    """
    Download holdings data for etfs in ishares website.

    Examples
    --------
    >>> from download_csv_from_link import (get_urls_from_ticker_list,
    ...     download_urls)
    >>> ticker_list = ['UEEH', 'IAEA', 'SUWU']
    >>> url_list = get_urls_from_ticker_list(ticker_list)
    >>> df_list = download_urls(url_list)

    """

    df_list = []
    for url_string in url_list:
        df_list.append(pd.read_csv(url_string, header=2))

    return(df_list)



