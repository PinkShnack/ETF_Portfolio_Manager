import pandas as pd
from portfolio import setup_data
from glob import glob


def get_holdings_urls_from_ticker_list(ticker_list, country="UK"):
    """
    Get http link for etfs in ishares website.

    Examples
    --------
    >>> from portfolio.io import get_holdings_urls_from_ticker_list
    >>> ticker_list = ['CSPX', 'IAEA', 'SUWU']
    >>> url_list = get_holdings_urls_from_ticker_list(ticker_list, "UK")
    >>> url_list[0]
    'https://www.ishares.com/uk/individual/en/products/253743/*/1506575576011.ajax?fileType=csv&fileName=CSPX_holdings&dataType=fund'

    >>> len(url_list)
    3

    >>> len(ticker_list)
    3

    >>> from portfolio.io import get_holdings_urls_from_ticker_list
    >>> ticker_list = ['EXXV', 'IUSU', 'IBCS'] #  german tickers
    >>> url_list = get_holdings_urls_from_ticker_list(ticker_list, "GER")
    >>> url_list[0]
    'https://www.ishares.com/uk/individual/en/products/253743/*/1506575576011.ajax?fileType=csv&fileName=CSPX_holdings&dataType=fund'

    """

    ticker_code_number_dict = setup_data.create_ticker_code_number_dict(
        country=country)

    chosen_tickers_dict = {}
    for k, v in ticker_code_number_dict.items():
        for ticker in ticker_list:
            if ticker == k:
                chosen_tickers_dict[k] = v
    
    url_list = []
    for key, val in chosen_tickers_dict.items():
        if "UK" in country:
            url_string = f"https://www.ishares.com/uk/individual/en/products/{val}/*/1506575576011.ajax?fileType=csv&fileName={key}_holdings&dataType=fund"
        elif "US" in country:
            url_string = f"https://www.ishares.com/us/products/{val}/*/1467271812596.ajax?fileType=csv&fileName={key}_holdings&dataType=fund"
        elif "GER" in country:
            url_string = f"https://www.ishares.com/de/privatanleger/de/produkte/{val}/*/1478358465952.ajax?fileType=csv&fileName={key}_holdings&dataType=fund"
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
    >>> from portfolio.io import (get_holdings_urls_from_ticker_list, download_urls)
    >>> ticker_list = ['UEEH', 'IAEA', 'SUWU']
    >>> url_list = get_holdings_urls_from_ticker_list(ticker_list)
    >>> df_list = download_urls(url_list)

    """

    df_list = []
    for url_string in url_list:
        df_list.append(pd.read_csv(url_string, header=2))

    return(df_list)


def load_tickers(ticker_list, country="UK", dummy_data=False):

    if dummy_data:
        # print("Grabbing Dummy Data")
        fnames = glob("dummy_data/*.csv")
        filenames = []
        for csv_file in fnames:
            for ticker in ticker_list:
                if ticker in csv_file:
                    filenames.append(csv_file)

        df_list = []
        for filename in filenames:
            df_list.append(pd.read_csv(filename, header=2))

    else:
        # print("Downloading ETF Data")
        df_list = download_urls(
            get_holdings_urls_from_ticker_list(ticker_list, country=country))

    return df_list
