'''


'''

# STANDARD LIBS
import sys;sys.path.append('..')
import io
from datetime import date

from typing import Any, Dict, List, Set, Union
import urllib.request as request

# THIRD PARTY LIBS
from bs4 import BeautifulSoup, ResultSet

import pandas 
from pandas.core.frame import DataFrame
import requests
from requests.models import Response

# CUSTOM LIBS
from batterypy.string.read import is_floatable, readf

# PROGRAM MODULES
from 

def get_sp_500() -> List[str]:
    r: Response = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    dfs: List[DataFrame] = pandas.read_html(r.text, header=0)
    stocks: List[str] = list(dfs[0].iloc[0:, 0])
    return stocks

def try_get_sp_500() -> List[str]:
    try:
        r: Response = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
        dfs: List[DataFrame] = pandas.read_html(r.text, header=0)
        stocks: List[str] = list(dfs[0].iloc[0:, 0])
        return stocks
    except requests.exceptions.RequestException as e:
        print('getsp500 error e:', e)
        return []
    except Exception as e2:
        print('get_sp_500 error e2:', e2)
        return []




def get_nasdaq_100() -> List[str]:
    try:
        r: Response = requests.get("https://en.wikipedia.org/wiki/NASDAQ-100")
        soup: BeautifulSoup = BeautifulSoup(r.text, 'html.parser')
        soup_item: ResultSet = soup.find('table', id='constituents')
        dfs: List[DataFrame] = pandas.read_html(str(soup_item), header=0)
        stocks: List[str] = list(dfs[0].iloc[0:, 1])
        return stocks
    except requests.exceptions.RequestException as e:
        print('get_nasdaq_100 error e:', e)
        return []
    except Exception as e2:
        print('get_nasdaq_100 error e2:', e2)
        return []




def get_nasdaq_listed() -> List[str]:
    try:
        url1 = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt'
        with request.urlopen(url1) as r:
            text = r.read().decode()
        df_nasdaq: DataFrame = pandas.read_csv(io.StringIO(text), sep='|', header=0)
        stocks: List[str] = list(df_nasdaq.iloc[:-1, 0])
        return stocks
    except Exception as e:
        print('get_nasdaq_listed error:', e)
        return []


def get_nasdaq_traded() -> List[str]:
    try:
        url1 = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqtraded.txt'
        with request.urlopen(url1) as r:
            text = r.read().decode()
        df_nasdaq: DataFrame = pandas.read_csv(io.StringIO(text), sep='|', header=0)
        stocks: List[str] = list(df_nasdaq.iloc[:-1, 1])
        return stocks
    except Exception as e:
        print('get_nasdaq_traded error:', e)
        return []


def get_option_traded() -> List[str]:
    """ file size is about 50mb, unique symbols are about 3129"""
    try:
        url1 = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/options.txt'
        with request.urlopen(url1) as r:
            text = r.read().decode()
        df_nasdaq: DataFrame = pandas.read_csv(io.StringIO(text), sep='|', header=0)
        stocks: List[str] = list(df_nasdaq.iloc[:-1, 0])
        stocks_set = sorted(list(set(stocks)))
        return stocks_set
    except Exception as e:
        print('get_option_traded error:', e)
        return []







if __name__ == '__main__':
    x = get_sp_500()

    print(x)
    
    print(f'{__file__} DONE')
