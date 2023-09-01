'''
*** INDEPENDENT MODULE ***

IMPORTED BY: 
    stock_guru_update/

'''

# STANDARD LIBS
import sys;sys.path.append('..')
import io

from typing import Any, Dict, List, Set, Union
import urllib.request as request

# THIRD PARTY LIBS
from bs4 import BeautifulSoup, ResultSet

import pandas 
from pandas.core.frame import DataFrame
import requests

# CUSTOM LIBS
from dimsumpy.web.crawler import get_html_dataframes, get_html_soup

# PROGRAM MODULES


def get_sp_500() -> List[str]:
    '''
    * INDEPENDENT *
    IMPORTS: dimsumpy
    '''
    sp_500_url: str = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    dfs: List[DataFrame] = get_html_dataframes(sp_500_url)
    stocks: List[str] = list(dfs[0].iloc[0:, 0])
    return stocks

def try_get_sp_500() -> List[str]:
    '''
    DEPENDS ON: get_sp_500()
    '''
    try:
        stocks: List[str] = get_sp_500()
        return stocks
    except requests.exceptions.RequestException as requests_error:
        print('try_get_sp_500 RequestException:', requests_error)
        return []
    except Exception as error:
        print('try_get_sp_500 general Exception:', error)
        return []




def get_nasdaq_100() -> List[str]:
    '''
    * INDEPENDENT *
    IMPORTS: pandas, dimsumpy
    '''
    nasdaq_100_url: str = 'https://en.wikipedia.org/wiki/NASDAQ-100'
    soup: BeautifulSoup = get_html_soup(nasdaq_100_url)
    soup_item: ResultSet = soup.find('table', id='constituents')
    dfs: List[DataFrame] = pandas.read_html(str(soup_item), header=0)
    stocks: List[str] = list(dfs[0].iloc[0:, 1])
    return stocks




def try_get_nasdaq_100() -> List[str]:
    '''
    DEPENDS ON: get_nasdaq_100()
    '''
    try:
        stocks: List[str] = get_nasdaq_100()
        return stocks
    except requests.exceptions.RequestException as e:
        print('get_nasdaq_100 error e:', e)
        return []
    except Exception as e2:
        print('get_nasdaq_100 error e2:', e2)
        return []



def get_nasdaq_listed() -> List[str]:
    '''
    * INDEPENDENT *
    IMPORTS: urllib, pandas
    '''

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
    '''
    * INDEPENDENT *
    IMPORTS: urllib, pandas
    '''
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
    '''
    * INDEPENDENT *
    IMPORTS: urllib, pandas
    file size is about 50mb, need several minutes to process, unique symbols are about 3129
    '''
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
