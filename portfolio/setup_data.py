import pandas as pd
import numpy as np
import os
from bs4 import BeautifulSoup


def dataframe_data_preparation(country="UK"):

    country_filename_csv, _ = get_filename_from_country(country=country)

    product_data_all = pd.read_csv(country_filename_csv, skiprows=[1])

    product_data_all['Ticker'].replace('-', np.nan, inplace=True)
    # product_data_all.head(3)

    if country == "GER":
        product_data_all["Name"] = product_data_all["Name der Anteilklasse"]

    product_data_ticker = product_data_all.dropna(subset=['Ticker'])
    # product_data_ticker.head(3)

    product_data_ticker.index = np.arange(0, len(product_data_ticker))
    # product_data_ticker.head(3)

    return product_data_ticker


def get_filename_from_country(country):
    '''

    Examples
    --------
    >>> from portfolio.setup_data import get_filename_from_country
    >>> filenames = get_filename_from_country("UK")

    '''

    if "UK" in country:
        country_filename_csv = "all_UK_products_ishares.csv"
        country_filename_html = "all_ishares_UK_etf_links.html"
    elif "US" in country:
        country_filename_csv = "all_US_products_ishares.csv"
        country_filename_html = "all_ishares_US_etf_links.html"
    elif "GER" in country:
        country_filename_csv = "all_Germany_products_ishares.csv"    
        country_filename_html = "all_ishares_Germany_etf_links.html"
    else:
        raise ValueError("`country` keyword must be 'UK', 'GER' or 'US'.")

    country_filename_csv = f"data/{country_filename_csv}"
    country_filename_html = f"data/{country_filename_html}"
    return country_filename_csv, country_filename_html


# Create ticker + name dict, ISIN + ticker dict
def create_ticker_name_dict(country="UK"):
    '''

    Examples
    --------
    >>> import portfolio.setup_data as setup_data
    >>> name_dict = setup_data.create_ticker_name_dict()

    '''
    df = dataframe_data_preparation(country=country)
    dict_ = dict(zip(df.Ticker, df.Name))
    return(dict_)


def create_ticker_ISIN_dict(country="UK"):
    df = dataframe_data_preparation(country=country)
    dict_ = dict(zip(df.Ticker, df.ISIN))
    return(dict_)


def create_ISIN_ticker_dict(country="UK"):
    df = dataframe_data_preparation(country=country)
    dict_ = dict(zip(df.ISIN, df.Ticker))
    return(dict_)


def get_info_using_ticker_list(ticker_list, output='name', country="UK"):
    '''

    Examples
    --------
    >>> import portfolio.setup_data as setup_data
    >>> info = setup_data.get_info_using_ticker_list(["IAEA"])

    '''
    if 'name' in output.lower():
        dict_ = create_ticker_name_dict(country=country)
    elif 'isin' in output.lower():
        dict_ = create_ticker_ISIN_dict(country=country)

    info = []
    for k, v in dict_.items():
        for ticker in ticker_list:
            if ticker == k:
                info.append(v)

    return info


def create_ticker_code_number_dict(country):

    _, country_filename_html = get_filename_from_country(country=country)
    print(country_filename_html)
    with open(country_filename_html, 'r', encoding='cp850') as html_file:
        source = html_file.read()

    soup = BeautifulSoup(source, 'html.parser')

    ticker_name_dict = create_ticker_name_dict()

    code_numbers = []
    tickers = []
    for link in soup.find_all('td', class_="links"):
        if link.text.upper() in ticker_name_dict.keys():
            tickers.append(link.text)
            full_href = link.find('a')
            just_href = full_href.get('href')
            code_number = just_href.split('/')[5]
            code_numbers.append(code_number)

    ticker_code_number_dict = dict(zip(tickers, code_numbers))
    return(ticker_code_number_dict)
