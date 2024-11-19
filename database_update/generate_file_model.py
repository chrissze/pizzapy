"""
*** INDEPENDENT MODULE ***

I can run this mode directly:

    (venv) $ python3 generate_file_model.py


"""

# STANDARD LIBS
import sys;sys.path.append('..')
from datetime import datetime
from functools import partial
from io import StringIO
import re
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







bank_stocks: List[str] = ['ASB', 'BAC', 'BK', 'C', 'CADE', 'CBSH', 'CFG', 'CFR', 'CMA', 'COF', 'COLB', 'DFS', 'EWBC', 'FFIN', 'FHN', 'FITB', 'FNB', 'GBCI', 'GS', 'HOMB', 'HWC', 'IBOC', 'JPM', 'HBAN', 'MS', 'MTB', 'NTRS', 'NYCB', 'KEY', 'ONB', 'OZK', 'PB', 'PNC', 'PNFP', 'RF', 'SCHW', 'SNV', 'SSB', 'STT', 'SYF', 'TCBI', 'TFC', 'UBSI', 'UMBF', 'USB', 'VLY', 'WBS', 'WFC', 'WTFC', 'ZION']

bank_stocks_set: Set[str] = set(bank_stocks)



def get_sp_400() -> Dict:
    """
    * INDEPENDENT *
    IMPORTS: dimsumpy
    execution time: 1 second
    """
    sp_400_url: str = 'https://en.wikipedia.org/wiki/List_of_S%26P_400_companies'
    dfs: List[DataFrame] = get_html_dataframes(sp_400_url)
    df = dfs[0]
    df.columns = ['Symbol', 'Company', 'Sector', 'Industry', 'Headquarters', 'Filing']
    stocks_dict = df.set_index('Symbol').to_dict(orient='index')
    return stocks_dict


def get_sp_500() -> Dict:
    """
    * INDEPENDENT *
    IMPORTS: dimsumpy
    execution time: 1 second

    The S&P 500 index undergoes a quarterly rebalancing to ensure it accurately reflects the U.S. large-cap equity market. These rebalancing events typically occur after third Friday of March, June, September, and December. 
    """
    sp_500_url: str = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    dfs: List[DataFrame] = get_html_dataframes(sp_500_url)
    df = dfs[0]
    df.columns = ['Symbol', 'Company', 'Sector', 'Industry', 'Headquarters', 'Added', 'CIK', 'Founded']
    stocks_dict = df.set_index('Symbol').to_dict(orient='index')
    return stocks_dict



def get_nasdaq_100() -> Any:
    """
    * INDEPENDENT *
    IMPORTS: dimsumpy
    execution time: 1 second

    Note: 
    I could not simply use get_html_dataframes() in this function, the html source structure is different.

    Nasdaq-100 Index undergoes an annual reconstitution in year end, usually November and December.
    2023 Additions: TTWO (20231218)
    2024 Additions: APP(20241118), PLTR(20241126)


    """
    nasdaq_100_url: str = 'https://en.wikipedia.org/wiki/NASDAQ-100'
    soup: BeautifulSoup = get_html_soup(nasdaq_100_url)
    soup_item: ResultSet = soup.find('table', id='constituents')
    dfs: List[DataFrame] = pandas.read_html(StringIO(str(soup_item)), header=0)
    df = dfs[0]
    df.columns = ['Company', 'Ticker', 'Sector', 'Industry']
    stocks_dict = df.set_index('Ticker').to_dict(orient='index')
    return stocks_dict



def get_sp_nasdaq() -> List[str]:
    """
    DEPENDS ON: get_sp_500(), get_nasdaq_100()
    USED BY: guru_operation_script.py

    The result is not including bank stocks.
    """
    sp_500_stocks: List[str] = list(get_sp_500().keys())
    sp_400_stocks: List[str] = list(get_sp_400().keys())
    nasdaq_100_stocks: List[str] = list(get_nasdaq_100().keys())
    sp_nasdaq_set: Set[str] = set(sp_500_stocks + sp_400_stocks + nasdaq_100_stocks)
    sp_nasdaq_stocks: List[str] = sorted(list(sp_nasdaq_set - bank_stocks_set))
    return sp_nasdaq_stocks





def get_nasdaq_listed() -> List[str]:
    """
    * INDEPENDENT *
    IMPORTS: urllib, pandas
    execution time: 4 seconds

    the initial_list has some nan values (without quotation marks)
    5,120 stocks on 2023-09-04
    """
    url1 = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt'
    with request.urlopen(url1) as r:
        text = r.read().decode()
    df_nasdaq: DataFrame = pandas.read_csv(StringIO(text), sep='|', header=0)
    initial_list: List[str] = list(df_nasdaq.iloc[:-1, 0])
    stock_list:List[str] = [item for item in initial_list if isinstance(item, str)]
    return stock_list


def get_nasdaq_traded() -> List[str]:
    """
    * INDEPENDENT *
    IMPORTS: urllib, pandas
    execution time: 5 second
    the initial_list has some nan values (without quotation marks)

    11,292 stock on 2023-09-04
    """
    url1 = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqtraded.txt'
    with request.urlopen(url1) as r:
        text = r.read().decode()
    df_nasdaq: DataFrame = pandas.read_csv(StringIO(text), sep='|', header=0)
    initial_list: List[str] = list(df_nasdaq.iloc[:-1, 1])
    stock_list:List[str] = [item for item in initial_list if isinstance(item, str)]
    return stock_list


def get_option_traded() -> List[str]:
    """
    * INDEPENDENT *
    IMPORTS: urllib, pandas
    execution time: 2 minutes
    file size is about 50mb, need several minutes to process, unique symbols are about 3129
    """
    url1 = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/options.txt'
    with request.urlopen(url1) as r:
        text = r.read().decode()
    df_nasdaq: DataFrame = pandas.read_csv(StringIO(text), sep='|', header=0)
    stocks: List[str] = list(df_nasdaq.iloc[:-1, 0])
    option_stocks: List[str] = sorted(list(set(stocks)))
    return option_stocks



def prepare_stock_list_file_content() -> str:
    """
    DEPENDS ON: get_sp_500(), get_sp_nasdaq(), get_nasdaq_100(),  get_nasdaq_listed(), get_nasdaq_traded(), get_option_traded()
    IMPORTS: datetime
    USED BY: generate_stock_list_file() 

    when I replace string BY re or replace('nan,', 'None,'), it will miss some items with special comma char, so I have to use ': nan'
    """
    current_time: datetime = datetime.now().replace(second=0, microsecond=0)
    file_comment: str = f'""" THIS FILE IS GENERATED AT {current_time} BY generate_stock_list_file() FUNCTION IN generate_file_model.py """'
    file_import: str = 'from typing import Dict, List'

    sp_500_dict: Dict =  get_sp_500()
    sp_500_dict_comment: str = f'# {len(sp_500_dict)}'
    sp_500_raw_string: str = f'sp_500_dict: Dict = {sp_500_dict}'
    sp_500_dict_variable: str = re.sub(': nan', ': None', sp_500_raw_string)

    sp_400_dict: Dict =  get_sp_400()
    sp_400_dict_comment: str = f'# {len(sp_400_dict)}'
    sp_400_raw_string: str = f'sp_400_dict: Dict = {sp_400_dict}'
    sp_400_dict_variable: str = re.sub(': nan', ': None', sp_400_raw_string)

    nasdaq_100_dict: Dict =  get_nasdaq_100()
    nasdaq_100_dict_comment: str = f'# {len(nasdaq_100_dict)}'
    nasdaq_100_dict_variable: str = f'nasdaq_100_dict: Dict = {nasdaq_100_dict}'

    sp_500: List[str] =  list(sp_500_dict.keys())
    sp_500_comment: str = f'# {len(sp_500)}'
    sp_500_variable: str = f'sp_500_stocks: List[str] = {sp_500}'
    
    sp_400: List[str] =  list(sp_400_dict.keys())
    sp_400_comment: str = f'# {len(sp_400)}'
    sp_400_variable: str = f'sp_400_stocks: List[str] = {sp_400}'

    nasdaq_100: List[str] = list(nasdaq_100_dict.keys())
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

    #option_traded: List[str] = get_option_traded()
    #option_traded_comment: str = f'# {len(option_traded)}'
    #option_traded_variable: str = f'option_traded_stocks: List[str] = {option_traded}'
    
    content: str = f'''
{file_comment}\n\n
{file_import}\n\n

{sp_500_dict_comment}
{sp_500_dict_variable}\n\n

{sp_400_dict_comment}
{sp_400_dict_variable}\n\n

{nasdaq_100_dict_comment}
{nasdaq_100_dict_variable}\n\n

{sp_500_comment}
{sp_500_variable}\n\n

{sp_400_comment}
{sp_400_variable}\n\n

{nasdaq_100_comment}
{nasdaq_100_variable}\n\n

{sp_nasdaq_comment}
{sp_nasdaq_variable}\n\n

{nasdaq_listed_comment}
{nasdaq_listed_variable}\n\n

{nasdaq_traded_comment}
{nasdaq_traded_variable}\n\n

'''
    return content



def generate_stock_list_file() -> None:
    """
    DEPENDS ON: prepare_stock_list_file_content()
    USED BY: terminal_scripts/central_script.py

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





def test_generated() -> None:
    def run() -> None:
        reply: str = input('Do you want to generate stock list module (yes/no)?')
        if reply == 'yes': 
            x =  generate_stock_list_file()
            print(x)

    seconds = timeit(run, number=1)
    print(seconds)
    print(f'{__file__} DONE')
    

def test() -> None:
    x = get_nasdaq_100()
    
    print(x)


if __name__ == '__main__':
    #test_generated()
    test()
