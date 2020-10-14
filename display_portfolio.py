
import os
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

# open a file,
# make the top row the row titles


ticker_name_dict = {
    'AYEM': 'MSCI EM IMI ESG ETF',
    'DGTL': 'Digitalisation ETF',
    'IQQH': 'Global Clean Energy ETF',
    'IS3S': 'MSCI World Value Factor',
    'IUSN': 'MSCI World Small Cap ETF',
    'SNAW': 'MSCI World ESG ETF',
    'SXRQ': 'Euro Gov Bond ETF 7-10yrs'}

ticker_percent_dict = {
    'AYEM': 10,
    'DGTL': 5,
    'IQQH': 5,
    'IS3S': 5,
    'IUSN': 10,
    'SNAW': 60,
    'SXRQ': 5}

get_portfolio_info(summarise="Sektor")
get_portfolio_info(summarise="Standort")
