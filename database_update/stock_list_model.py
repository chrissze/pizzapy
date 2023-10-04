"""
*** INDEPENDENT MODULE ***

USED BY: 
    core_stock_update/

"""

# STANDARD LIBS
import sys;sys.path.append('..')
from datetime import datetime
from functools import partial
import io
import subprocess
from timeit import timeit
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
from database_update.generated_stock_list import nasdaq_100_stocks, nasdaq_listed_stocks, nasdaq_traded_stocks, option_traded_stocks, sp_500_stocks, sp_nasdaq_stocks


from database_update.postgres_command_model import guru_stock_create_table_command, zacks_stock_create_table_command, stock_option_create_table_command, stock_price_create_table_command, stock_technical_create_table_command, futures_option_create_table_command

from guru_stock_update.guru_update_database_model import upsert_guru
from stock_option_update.option_update_database_model import upsert_option
from zacks_stock_update.zacks_update_database_model import upsert_zacks
from stock_price_update.price_update_database_model import upsert_latest_price
from stock_price_update.technical_update_database_model import upsert_recent_technical, upsert_technical_one






# need to comment out all_stocks when I use code to generate 
all_stocks: List[str] = nasdaq_traded_stocks + ['FNMA', 'FMCC']

stock_list_dict: Dict[str, List[str]] = {
    f'Nasdaq 100 ({len(nasdaq_100_stocks)})': nasdaq_100_stocks,
    f'S&P 500 ({len(sp_500_stocks)})': sp_500_stocks,
    f'S&P 500 + Nasdqa 100 ({len(sp_nasdaq_stocks)})': sp_nasdaq_stocks,
    f'Option Stocks ({len(option_traded_stocks)})': option_traded_stocks,
    f'Nasdaq Listed ({len(nasdaq_listed_stocks)})': nasdaq_listed_stocks,
    f'Nasdaq Traded ({len(nasdaq_traded_stocks)})': nasdaq_traded_stocks,
    f'All Stocks ({len(all_stocks)})': all_stocks,
}


# This dictionary can be used to compose upsert commands
# option, price and technicals are from yahoo
table_function_dict: Dict[str, Any] = {
    'guru_stock': upsert_guru ,
    'zacks_stock': upsert_zacks,
    'stock_option': upsert_option,
    'stock_price': upsert_latest_price,
    'stock_technical': upsert_recent_technical,
    'technical_one': upsert_technical_one,
    'futures_option': upsert_guru ,
}




def get_sp_500() -> List[str]:
    """
    * INDEPENDENT *
    IMPORTS: dimsumpy
    execution time: 1 second
    """
    sp_500_url: str = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    dfs: List[DataFrame] = get_html_dataframes(sp_500_url)
    stocks: List[str] = list(dfs[0].iloc[0:, 0])
    return stocks




def get_nasdaq_100() -> List[str]:
    """
    * INDEPENDENT *
    IMPORTS: pandas, dimsumpy
    execution time: 1 second
    """
    nasdaq_100_url: str = 'https://en.wikipedia.org/wiki/NASDAQ-100'
    soup: BeautifulSoup = get_html_soup(nasdaq_100_url)
    soup_item: ResultSet = soup.find('table', id='constituents')
    dfs: List[DataFrame] = pandas.read_html(str(soup_item), header=0)
    stocks: List[str] = list(dfs[0].iloc[0:, 1])
    return stocks


def get_sp_nasdaq() -> List[str]:
    """
    DEPENDS ON: get_sp_500(), get_nasdaq_100()
    USED BY: guru_operation_script.py
    """
    sp_500_stocks: List[str] = get_sp_500()
    nasdaq_100_stocks: List[str] = get_nasdaq_100()
    sp_nasdaq_stocks: List[str] = sorted(list(set(sp_500_stocks + nasdaq_100_stocks)))
    return sp_nasdaq_stocks





def get_nasdaq_listed() -> List[str]:
    """
    * INDEPENDENT *
    IMPORTS: urllib, pandas
    execution time: 4 seconds

    the initial_list has some nan values (without quotation marks)
    5,120 stocks on 2023-09-04
    """

    try:
        url1 = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt'
        with request.urlopen(url1) as r:
            text = r.read().decode()
        df_nasdaq: DataFrame = pandas.read_csv(io.StringIO(text), sep='|', header=0)
        initial_list: List[str] = list(df_nasdaq.iloc[:-1, 0])
        stock_list:List[str] = [item for item in initial_list if isinstance(item, str)]
        return stock_list
    except Exception as e:
        print('get_nasdaq_listed error:', e)
        return []


def get_nasdaq_traded() -> List[str]:
    """
    * INDEPENDENT *
    IMPORTS: urllib, pandas
    execution time: 5 second
    the initial_list has some nan values (without quotation marks)

    11,292 stock on 2023-09-04
    """
    try:
        url1 = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqtraded.txt'
        with request.urlopen(url1) as r:
            text = r.read().decode()
        df_nasdaq: DataFrame = pandas.read_csv(io.StringIO(text), sep='|', header=0)
        initial_list: List[str] = list(df_nasdaq.iloc[:-1, 1])
        stock_list:List[str] = [item for item in initial_list if isinstance(item, str)]
        return stock_list
    except Exception as e:
        print('get_nasdaq_traded error:', e)
        return []


def get_option_traded() -> List[str]:
    """
    * INDEPENDENT *
    IMPORTS: urllib, pandas
    execution time: 2 minutes
    file size is about 50mb, need several minutes to process, unique symbols are about 3129
    """
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



def prepare_stock_list_file_content() -> str:
    """
    DEPENDS ON: get_sp_500(), get_sp_nasdaq(), get_nasdaq_100(),  get_nasdaq_listed(), get_nasdaq_traded(), get_option_traded()
    IMPORTS: datetime
    USED BY: generate_stock_list_module() 
    """
    current_time: datetime = datetime.now().replace(second=0, microsecond=0)
    file_comment: str = f'""" THIS FILE IS GENERATED AT {current_time} BY generate_stock_list_module() """'
    file_import: str = 'from typing import List'

    sp_500: List[str] = get_sp_500()
    sp_500_comment: str = f'# {len(sp_500)}'
    sp_500_variable: str = f'sp_500_stocks: List[str] = {sp_500}'

    nasdaq_100: List[str] = get_nasdaq_100()
    nasdaq_100_comment: str = f'# {len(nasdaq_100)}'
    nasdaq_100_variable: str = f'nasdaq_100_stocks: List[str] = {nasdaq_100}'

    sp_nasdaq: List[str] = get_sp_nasdaq()
    sp_nasdaq_comment: str = f'# {len(sp_nasdaq)}'
    sp_nasdaq_variable: str = f'sp_nasdaq_stocks: List[str] = {sp_nasdaq}'

    nasdaq_listed: List[str] = get_nasdaq_listed()
    nasdaq_listed_comment: str = f'# {len(nasdaq_listed)}'
    nasdaq_listed_variable: str = f'nasdaq_listed_stocks: List[str] = {nasdaq_listed}'
    
    nasdaq_traded: List[str] = get_nasdaq_traded()
    nasdaq_traded_comment: str = f'# {len(nasdaq_traded)}'
    nasdaq_traded_variable: str = f'nasdaq_traded_stocks: List[str] = {nasdaq_traded}'

    option_traded: List[str] = get_option_traded()
    option_traded_comment: str = f'# {len(option_traded)}'
    option_traded_variable: str = f'option_traded_stocks: List[str] = {option_traded}'
    
    content: str = f'''
{file_comment}\n\n
{file_import}\n\n

{sp_500_comment}
{sp_500_variable}\n\n

{nasdaq_100_comment}
{nasdaq_100_variable}\n\n

{sp_nasdaq_comment}
{sp_nasdaq_variable}\n\n

{nasdaq_listed_comment}
{nasdaq_listed_variable}\n\n

{nasdaq_traded_comment}
{nasdaq_traded_variable}\n\n

{option_traded_comment}
{option_traded_variable}\n\n
'''
    return content



def generate_stock_list_module() -> None:
    """
    DEPENDS ON: prepare_stock_list_file_content()
    execution time: 4 minutes due to get_option_traded() and black command
    When I re-run this file, it will overwrite the original content
    """
    filename = 'generated_stock_list.py'
    print(f'Generated {filename} now ...')
    content: str = prepare_stock_list_file_content()
    with open(filename, 'w') as f:
        f.write(content)
    print(f'write {filename} done, now using black to format it according to PEP8...')
    black_cmd = f'black {filename}'
    subprocess.run(black_cmd, stdin=True, shell=True)
    print('ALL DONE')
    return None





def test_generated_stock_list_module() -> None:
    def run() -> None:
        reply: str = input('Do you want to generate stock list module (yes/no)?')
        if reply == 'yes': 
            x =  generate_stock_list_module()
            print(x)

    seconds = timeit(run, number=1)
    print(seconds)
    print(f'{__file__} DONE')
    

def test() -> None:
    print('test')

if __name__ == '__main__':
    test()
