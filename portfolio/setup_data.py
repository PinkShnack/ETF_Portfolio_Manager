import pandas as pd
import numpy as np
import os
from bs4 import BeautifulSoup


path_to_data = os.path.join(os.path.dirname(''), 'data')
os.chdir(path_to_data)

product_data_all = pd.read_csv("product-screener.csv", skiprows=[1])
# product_data_all.head(3)

product_data_all['Ticker'].replace('-', np.nan, inplace=True)
# product_data_all.head(3)

product_data_ticker = product_data_all.dropna(subset=['Ticker'])
# product_data_ticker.head(3)

product_data_ticker.index = np.arange(0, len(product_data_ticker))
# product_data_ticker.head(3)


# Create ticker + name dict, ISIN + ticker dict
def create_ticker_name_dict(df=product_data_ticker):
    dict_ = dict(zip(df.Ticker, df.Name))
    return(dict_)


def create_ticker_ISIN_dict(df=product_data_ticker):
    dict_ = dict(zip(df.Ticker, df.ISIN))
    return(dict_)


def create_ISIN_ticker_dict(df=product_data_ticker):
    dict_ = dict(zip(df.ISIN, df.Ticker))
    return(dict_)


def get_info_using_ticker_list(ticker_list, output='name'):
    if 'name' in output.lower():
        dict_ = create_ticker_name_dict()
    elif 'isin' in output.lower():
        dict_ = create_ticker_name_dict()

    info = []
    for k, v in dict_.items():
        for ticker in ticker_list:
            if ticker == k:
                info.append(v)

    return info


def create_ticker_code_number_dict(
        file='all_ishares_uk_etf_links.html'):

    with open(file, 'r', encoding='cp850') as html_file:
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
