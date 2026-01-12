


"""


initialize_guru > gather_guru > finalize_guru > upsert_guru

"""


# STANDARD LIBRARIES

import asyncio

from datetime import date, datetime

from itertools import dropwhile

import json

from multiprocessing import Manager, Process

from multiprocessing.managers import DictProxy, SyncManager

import re

from timeit import default_timer

from typing import Any, Dict, List, Optional, Tuple



# THIRD PARTY LIBRARIES

import asyncpg

from asyncpg import Record


from bs4 import BeautifulSoup

from bs4.element import ResultSet, Tag

import pandas as pd

from pandas import DataFrame

import requests


# CUSTOM LIBRARIES

from batterypy.read import formatlarge, readf

from batterypy.cal import get_trading_day_utc

from dimsumpy.web.crawler import get_html_soup, get_html_text, get_html_dataframes












######################################################
### 1ST PHASE : INITIALIZE_GURU WITH PRICE AND CAP ###
######################################################


def extract_nested_values(obj, key):
    """
    ** INDEPENDENT **
    
    USED BY: get_barchart_price_cap
     
    Pull all values of specified key from nested JSON.
    
    Source:
       https://hackersandslackers.com/extract-data-from-complex-json-python/ 
       
    """

    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results



def get_barchart_price_cap(symbol: str) -> Tuple[Optional[float], Optional[float]] :
    """
    DEPENDS: extract_nested_values

    IMPORTS: json, beautifulsoup4, batterypy, dimsumpy
        
    I can use this function to display the marketcap dictionary in formatted string:
        json_cap_pretty: str = json.dumps(json_cap, indent=2)

    """
    barchart_url: str = f'https://www.barchart.com/stocks/quotes/{symbol}'
    barchart_soup: BeautifulSoup = get_html_soup(barchart_url)
    # soup.find function below is safe, it will return None if it cannot find the target.
    price_soup_items: Optional[Tag] = barchart_soup.find('div', attrs={'data-ng-controller': 'symbolHeaderCtrl'})
    price_item: Optional[str] = price_soup_items.get('data-ng-init') if price_soup_items else None
    json_price: Optional[Dict[str, Any]] = json.loads(price_item[5:-1]) if price_item else None
    price: Optional[float] = readf(json_price.get('lastPrice')) if json_price else None

    cap_soup_items: ResultSet = barchart_soup.find('script', id='bc-dynamic-config')
    json_cap: Dict[str, Any] = json.loads(cap_soup_items.string)
    marketcaps: List[Any] = extract_nested_values(json_cap, 'marketCap')
    cap: Optional[float] = None if len(marketcaps) < 3 else readf(marketcaps[2])
    return price, cap


    

def initialize_guru(symbol: str) -> DictProxy:
    """
        
        IMPORTS: multiprocessing(DictProxy, SyncManager)
        DEPENDS: get_barchart_price_cap
        
        USED BY: make_option_proxy()

        I write `is not None` for testing below since price, cap might be 0, which is a false value.
    """
    manager: SyncManager = Manager()
    proxy: DictProxy = manager.dict()
    proxy['symbol'] = symbol
    proxy['td'] = get_trading_day_utc()
    proxy['t'] = datetime.now().replace(second=0, microsecond=0)

    price: Optional[float]
    cap: Optional[float]
    price, cap = get_barchart_price_cap(symbol)    
    proxy['price'] = price
    proxy['cap'] = cap
    proxy['cap_str'] = formatlarge(cap) if cap is not None else None
    return proxy


### END OF 1ST PHASE : INITIALIZE_GURU WITH PRICE AND CAP ###





###############################
### 2ND PHASE : GATHER_GURU ###
###############################



def get_guru_book_value(symbol: str) -> Optional[float]:
    """
    The returning value is Tangible Book Value Per Share.

    https://www.gurufocus.com/term/tangibles-book-per-share/AMD
    
Tangible book value per share is calculated as the total tangible equity divided by Shares Outstanding. Total tangible equity is calculated as the Total Stockholders Equity minus Preferred Stock minus Intangible Assets. 

https://www.gurufocus.com/term/Tangibles_book_per_share/NVDA/Tangible-Book-per-Share/

Try or not try? this module's proxy_guru_book_value() does not use try block,
this function is used in the last chain function in guru_proxy_model.py,
it is much faster to run 10 functions at the same time without nested try blocks.

"""

    book_value_url: str = f'https://www.gurufocus.com/term/tangibles-book-per-share/{symbol}'
    
    book_value_dfs: List[DataFrame] = get_html_dataframes(book_value_url)
    book_value_str: Any = '' if len(book_value_dfs) < 3 or book_value_dfs[1].empty else book_value_dfs[1].iloc[-1, -1] 
    book_value: Optional[float] = readf(book_value_str)
    return book_value




def proxy_guru_book_value(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
    DEPENDS ON: get_guru_book_value
    
    USED BY: gather_guru

    I use `is not None` to test because 0.0 is false.
    No need to use try block, as the last chaining function used this function will have tried.  
    """
    book_value: Optional[float] = get_guru_book_value(symbol)
    proxy['book_value'] = book_value

    book_value_pc: Optional[float] = round((book_value / proxy['price'] * 100.0), 2) if (proxy.get('price') and book_value) else None
    proxy['book_value_pc'] = book_value_pc
    return proxy





def get_guru_debt_per_share(symbol: str) -> Optional[float]:

    """ 
    REQUIRES: pandas

    TTWO debt is 0.00 with tables, ttwo's debt is really 0.00
        USO is None
    
        https://www.gurufocus.com/term/total-debt-per-share/NVDA

    """
    debt_url: str = f'https://www.gurufocus.com/term/total-debt-per-share/{symbol}'

    debt_dfs: List[DataFrame] = get_html_dataframes(debt_url)

    debt_str: Any = '' if len(debt_dfs) < 3 or debt_dfs[1].empty else debt_dfs[1].iloc[-1, -1] # can be str or float64 type

    debt_per_share: Optional[float] = readf(debt_str)

    return debt_per_share




def proxy_guru_debt(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
    DEPENDS: try_get_guru_debt_per_share > get_guru_debt_per_share
    try_get_guru_debt_per_share() can be changed to get_guru_debt_per_share()
    """
    debt_per_share: Optional[float]  = get_guru_debt_per_share(symbol)
    proxy['debt_per_share'] = debt_per_share

    debt_pc: Optional[float] = round((debt_per_share / proxy['price'] * 100.0), 2) if (proxy.get('price') and debt_per_share) else None
    proxy['debt_pc'] = debt_pc
    return proxy





def get_guru_earn_per_share(symbol: str, d: DictProxy={}) -> Optional[float]:
    """
    REQUIRES: beautifulsoup4

    https://www.gurufocus.com/term/eps-without-nri/NVDA
    
    """
    earn_url: str = f'https://www.gurufocus.com/term/eps-without-nri/{symbol}'
    earn_soup: BeautifulSoup = get_html_soup(earn_url)
    earn_soup_items: ResultSet = earn_soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not earn_soup_items else earn_soup_items[0].get('content')
    earn_strlist: List[str] = content.split()
    earn_strlist2: List[str] = list(filter(lambda x: '$' in x, earn_strlist))
    earn_per_share: Optional[float] = readf(earn_strlist2[0][:-1]) if earn_strlist2 else None
    return earn_per_share


def get_guru_buyback_yield(symbol: str, d: DictProxy={}) -> Optional[float]:
    """
    REQUIRES: 

    https://www.gurufocus.com/term/buyback-yield/AAPL

    """
    buyback_yield_url: str = f'https://www.gurufocus.com/term/buyback-yield/{symbol}'
    soup: BeautifulSoup = get_html_soup(buyback_yield_url)
    soup_items: ResultSet = soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not soup_items else soup_items[0].get('content')

    strlist: List[str] = content.split()

    strlist2: List[str] = list(filter(lambda x: '.' in x, strlist))

    buyback_yield: Optional[float] = readf(strlist2[0][:-1]) if strlist2 else None
    
    #print(f'{content=}')
    #print(f'{strlist2=}')
    #print(f'{buyback_yield=}')
    return buyback_yield


def get_guru_dividend_yield(symbol: str, d: DictProxy={}) -> Optional[float]:
    """
    REQUIRES: 

    https://www.gurufocus.com/term/yield/EQR

    """
    dividend_yield_url: str = f'https://www.gurufocus.com/term/yield/{symbol}'
    soup: BeautifulSoup = get_html_soup(dividend_yield_url)
    soup_items: ResultSet = soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not soup_items else soup_items[0].get('content')

    strlist: List[str] = content.split()

    strlist2: List[str] = list(filter(lambda x: '%.' in x, strlist))

    dividend_yield: Optional[float] = readf(strlist2[0][:-1]) if strlist2 else None
    
    #print(f'{content=}')
    #print(f'{strlist2=}')
    #print(f'{dividend_yield=}')
    return dividend_yield





def get_guru_earn_yield(symbol: str, d: DictProxy={}) -> Optional[float]:
    """
    REQUIRES: 

    https://www.gurufocus.com/term/earning-yield/NVDA

    """
    earn_url: str = f'https://www.gurufocus.com/term/earning-yield/{symbol}'
    earn_soup: BeautifulSoup = get_html_soup(earn_url)
    earn_soup_items: ResultSet = earn_soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not earn_soup_items else earn_soup_items[0].get('content')

    earn_strlist: List[str] = content.split()

    earn_strlist2: List[str] = list(filter(lambda x: '%.' in x, earn_strlist))

    earn_yield: Optional[float] = readf(earn_strlist2[0][:-1]) if earn_strlist2 else None
    
    #print(content)
    #print(f'{earn_strlist2=}')
    #print(f'{earn_yield=}')
    return earn_yield



def get_guru_fcf_yield(symbol: str, d: DictProxy={}) -> Optional[float]:
    """
    REQUIRES: 

    https://www.gurufocus.com/term/fcf-yield/NVDA

    """
    fcf_yield_url: str = f'https://www.gurufocus.com/term/fcf-yield/{symbol}'
    soup: BeautifulSoup = get_html_soup(fcf_yield_url)
    soup_items: ResultSet = soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not soup_items else soup_items[0].get('content')

    strlist: List[str] = content.split()

    strlist2: List[str] = list(filter(lambda x: '.' in x, strlist))

    fcf_yield: Optional[float] = readf(strlist2[0][:-1]) if strlist2 else None
    
    #print(f'{content=}')
    #print(f'{strlist2=}')
    #print(f'{fcf_yield=}')
    return fcf_yield



def get_guru_pay_debt_yield(symbol: str, d: DictProxy={}) -> Optional[float]:
    """
    REQUIRES: 

    https://www.gurufocus.com/term/net-debt-paydown-yield/NVDA

    https://www.gurufocus.com/term/net-debt-paydown-yield/MU

    Negative number means debt burden increase, see MU.

    """
    pay_debt_yield_url: str = f'https://www.gurufocus.com/term/net-debt-paydown-yield/{symbol}'
    soup: BeautifulSoup = get_html_soup(pay_debt_yield_url)
    soup_items: ResultSet = soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not soup_items else soup_items[0].get('content')

    strlist: List[str] = content.split()

    strlist2: List[str] = list(filter(lambda x: '%.' in x, strlist))

    pay_debt_yield: Optional[float] = readf(strlist2[0][:-1]) if strlist2 else None
    
    #print(f'{content=}')
    #print(f'{strlist2=}')
    #print(f'{pay_debt_yield=}')
    return pay_debt_yield


def get_guru_payout_yield(symbol: str, d: DictProxy={}) -> Optional[float]:
    """
    REQUIRES: 

    https://www.gurufocus.com/term/total-payout-yield/NVDA

    Total Payout Yield is the percent a company has paid to its shareholders through net repurchases of shares and dividends based on its Market Cap. 

    """
    payout_yield_url: str = f'https://www.gurufocus.com/term/total-payout-yield/{symbol}'
    soup: BeautifulSoup = get_html_soup(payout_yield_url)
    soup_items: ResultSet = soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not soup_items else soup_items[0].get('content')

    strlist: List[str] = content.split()

    strlist2: List[str] = list(filter(lambda x: '.' in x, strlist))

    payout_yield: Optional[float] = readf(strlist2[0][:-1]) if strlist2 else None
    
    print(f'{content=}')
    print(f'{strlist2=}')
    print(f'{payout_yield=}')
    return payout_yield




def get_guru_shareholder_yield(symbol: str, d: DictProxy={}) -> Optional[float]:
    """
    REQUIRES: 

    https://www.gurufocus.com/term/shareholder-yield/NVDA

    hareholder-yield

    Shareholder Yield is how much money shareholders receive from a company that is in the form of 
    1. cash dividends 
    2. net stock repurchases
    3. debt reduction. 

Copied from: NVDA (NVIDIA) Shareholder Yield % - <https://www.gurufocus.com/term/shareholder-yield/NVDA>

    """
    shareholder_yield_url: str = f'https://www.gurufocus.com/term/shareholder-yield/{symbol}'
    soup: BeautifulSoup = get_html_soup(shareholder_yield_url)
    soup_items: ResultSet = soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not soup_items else soup_items[0].get('content')

    strlist: List[str] = content.split()

    strlist2: List[str] = list(filter(lambda x: '%.' in x, strlist))

    shareholder_yield: Optional[float] = readf(strlist2[0][:-1]) if strlist2 else None
    
    #print(f'{content=}')
    #print(f'{strlist2=}')
    #print(f'{shareholder_yield=}')
    return shareholder_yield


def get_guru_roic(symbol: str, d: DictProxy={}) -> Optional[float]:
    """
    REQUIRES: 

    https://www.gurufocus.com/term/roic/META

    """
    roic_url: str = f'https://www.gurufocus.com/term/roic/{symbol}'
    soup: BeautifulSoup = get_html_soup(roic_url)
    soup_items: ResultSet = soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not soup_items else soup_items[0].get('content')

    strlist: List[str] = content.split()

    strlist2: List[str] = list(filter(lambda x: '%.' in x, strlist))

    roic: Optional[float] = readf(strlist2[0][:-1]) if strlist2 else None
    #print(f'{content=}')
    #print(f'{strlist2=}')
    #print(f'{roic=}')
    return roic




def get_guru_wacc(symbol: str, d: DictProxy={}) -> Optional[float]:
    """
    REQUIRES:

    https://www.gurufocus.com/term/wacc/META

    """
    wacc_url: str = f'https://www.gurufocus.com/term/wacc/{symbol}'
    soup: BeautifulSoup = get_html_soup(wacc_url)
    soup_items: ResultSet = soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not soup_items else soup_items[0].get('content')

    strlist: List[str] = content.split()

    strlist2: List[str] = list(filter(lambda x: '%.' in x, strlist))

    wacc: Optional[float] = readf(strlist2[0][:-1]) if strlist2 else None
    #print(f'{content=}')
    #print(f'{strlist2=}')
    #print(f'{wacc=}')
    return wacc




def proxy_guru_earn(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS: try_get_guru_earn_per_share > get_guru_earn_per_share"""

    earn_per_share: Optional[float]  = get_guru_earn_per_share(symbol)

    proxy['earn_per_share'] = earn_per_share
    earn_pc: Optional[float] = round((earn_per_share / proxy['price'] * 100.0), 2) if (proxy.get('price') and earn_per_share) else None

    proxy['earn_pc'] = earn_pc
    proxy['buyback_yield'] = get_guru_buyback_yield(symbol)
    proxy['dividend_yield'] = get_guru_dividend_yield(symbol)
    proxy['earn_yield'] = get_guru_earn_yield(symbol)
    proxy['fcf_yield'] = get_guru_fcf_yield(symbol)
    proxy['pay_debt_yield'] = get_guru_pay_debt_yield(symbol)
    proxy['payout_yield'] = get_guru_payout_yield(symbol)
    proxy['roic'] = get_guru_roic(symbol)
    proxy['shareholder_yield'] = get_guru_shareholder_yield(symbol)
    proxy['wacc'] = get_guru_wacc(symbol)
    return proxy







def get_guru_equity(SYMBOL: str) -> Optional[float]:
    """

    https://www.gurufocus.com/term/total-stockholders-equity/NVDA
    """
    equity_url: str = f'https://www.gurufocus.com/term/total-stockholders-equity/{SYMBOL}'
    equity_soup: BeautifulSoup = get_html_soup(equity_url)
    equity_soup_items: ResultSet = equity_soup.find_all('meta', attrs={'name': 'description'})
    
    content: str = equity_soup_items[0].get('content') if equity_soup_items else ''
    equity_strlist: List[str] = content.split()
    equity_strlist_shortened: List[str] = list(dropwhile(lambda x: x != 'is', equity_strlist))    

    equity_in_million: Optional[float] = None if len(equity_strlist_shortened) < 3 else readf(equity_strlist_shortened[1])
    equity: Optional[float] = None if equity_in_million is None else abs(equity_in_million) * 1000000.0
    equity: Optional[float] = equity_in_million * 1000000.0 if equity_in_million else None
    return equity





def proxy_guru_equity(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS: try_get_guru_equity > get_guru_equity"""
    equity: Optional[float]  = get_guru_equity(symbol)
    proxy['equity'] = equity
    equity_pc: Optional[float] = round((equity / proxy['cap'] * 100.0), 4) if proxy.get('cap') and equity else None
    proxy['equity_pc'] = equity_pc
    return proxy







def get_guru_interest(symbol: str) -> Optional[float]:
    """    

    https://www.gurufocus.com/term/interest-expense/NVDA
    """

    interest_url: str = f'https://www.gurufocus.com/term/interest-expense/{symbol}'
    
    interest_dfs: List[DataFrame] = get_html_dataframes(interest_url)

    interest_str: Any = '' if len(interest_dfs) < 3 or interest_dfs[0].empty else interest_dfs[0].iloc[-1, -1] 
    
    negative_interest_in_million: Optional[float] = readf(interest_str)

    interest: Optional[float] = None if negative_interest_in_million is None else abs(negative_interest_in_million) * 1000000.0
    
    return interest






def proxy_guru_interest(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS: try_get_guru_interest > get_guru_interest"""
    interest: Optional[float]  = get_guru_interest(symbol)
    proxy['interest'] = interest
    
    interest_pc: Optional[float] = round((interest / proxy['cap'] * 100.0), 4) if (proxy.get('cap') and interest) else None
    proxy['interest_pc'] = interest_pc
    return proxy






def get_guru_lynch(symbol: str) -> Optional[float]:
    """
    Lynch Value is Peter Lynch's estimation of fair price
    
    https://www.gurufocus.com/term/peter-lynch-fair-value/NVDA
    """

    lynch_url: str = f'https://www.gurufocus.com/term/peter-lynch-fair-value/{symbol}'

    soup: BeautifulSoup = get_html_soup(lynch_url)

    soup_items: ResultSet = soup.find_all('meta', attrs={'name': 'description'})

    content: str = '' if not soup_items else soup_items[0].get('content')

    strlist: List[str] = content.split()
    #print(strlist)

    strlist_shortened: List[str] = list(dropwhile(lambda x: x != 'is', strlist))    

    lynch: Optional[float] = None if len(strlist_shortened) < 3 else readf(strlist_shortened[1])

    return lynch



def proxy_guru_lynch(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS: try_get_guru_lynch > get_guru_lynch
    
    lynch is Peter Lynch's fair price.

    lynchmove is the expected movement in percentage, 20.0 means expecting to have 20% price increase; -30 means expecting to have 20% price drop.
    
    try_get_guru_lynch() below can be changed to get_guru_lynch()
    """
    lynch: Optional[float]  = get_guru_lynch(symbol)   
    proxy['lynch'] = lynch

    lynch_move_pc: Optional[float] = round((lynch - proxy['price']) / proxy['price'] * 100.0, 2) if (proxy.get('price') and lynch) else None
    proxy['lynch_move_pc'] = lynch_move_pc
    return proxy





def get_guru_net_capital(symbol: str) -> Optional[float]:
    """
    net_capital here is (cash equivalent + Receivable * certain percentage + inventory * percentage - total debt)
    
    https://www.gurufocus.com/term/net-net-working-capital/NVDA
    """
    
    net_capital_url: str = f'https://www.gurufocus.com/term/net-net-working-capital/{symbol}'
    
    net_capital_dfs: List[DataFrame] = get_html_dataframes(net_capital_url)
    
    # net_capital_value can be str or float64 type
    net_capital_value: Any = '' if len(net_capital_dfs) < 3 or net_capital_dfs[1].empty else net_capital_dfs[1].iloc[-1, -1]
    
    net_capital: Optional[float] = readf(net_capital_value)
    
    return net_capital




def proxy_guru_net_capital(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
    DEPENDS: try_get_guru_net_capital > get_guru_net_capital
    try_get_guru_net_capital() can be changed to get_guru_net_capital()
    """
    net_capital: Optional[float] = get_guru_net_capital(symbol)
    proxy['net_capital'] = net_capital

    net_capital_pc: Optional[float] = round((net_capital / proxy['price'] * 100.0), 2) if (proxy.get('price') and net_capital) else None
    proxy['net_capital_pc'] = net_capital_pc
    return proxy




def get_guru_net_margin(symbol: str) -> Optional[float]:
    """
    
    https://www.gurufocus.com/term/net-margin/MSFT
    https://www.gurufocus.com/term/net-margin/NVDA
    """
    
    net_margin_url: str = f'https://www.gurufocus.com/term/net-margin/{symbol}'
    
    net_margin_dfs: List[DataFrame] = get_html_dataframes(net_margin_url)
    
    # net_margin_value can be str or float64 type
    net_margin_value: Any = '' if len(net_margin_dfs) < 3 or net_margin_dfs[1].empty else net_margin_dfs[1].iloc[-1, -1]
    
    net_margin: Optional[float] = readf(net_margin_value)
    
    return net_margin




def proxy_guru_net_margin(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
    DEPENDS: get_guru_net_margin
    """
    net_margin: Optional[float] = get_guru_net_margin(symbol)
    proxy['net_margin'] = net_margin
    return proxy




def get_guru_research(symbol: str) -> Optional[float]:
    """
    Research & Development expense

    https://www.gurufocus.com/term/research-development/NVDA
    """
    research_url: str = f'https://www.gurufocus.com/term/research-development/{symbol}'
    
    research_soup: BeautifulSoup = get_html_soup(research_url)

    research_soup_items: ResultSet = research_soup.find_all('meta', attrs={'name': 'description'})
    
    content: str = '' if not research_soup_items else research_soup_items[0].get('content')
    
    strlist: List[str] = content.split()
    #print(strlist)

    short_strlist: List[str] = list(dropwhile(lambda x: x != 'is', strlist))    
    
    research_in_million: Optional[float] = None if len(short_strlist) < 3 else readf(short_strlist[1])
    
    research: Optional[float] = None if research_in_million is None else research_in_million * 1000000
    
    return research





def proxy_guru_research(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS: try_get_guru_research > get_guru_research"""
    research: Optional[float] = get_guru_research(symbol)
    proxy['research'] = research
    
    research_pc: Optional[float] = round((research / proxy['cap'] * 100.0), 2) if (proxy.get('cap') and research) else None
    proxy['research_pc'] = research_pc
    return proxy



def get_guru_revenue_per_share(symbol: str) -> Optional[float]:
    """
    returns Revenue Per Share

    https://www.gurufocus.com/term/revenue-per-share/NVDA
    
        NVIDA has 1, 3, 5, 10 years average growth rates. 
        https://www.gurufocus.com/term/per+share+rev/NVDA/Revenue-per-Share/

        COINBASE has only 1 and 3 years average grow rates (last update: 2023)
        https://www.gurufocus.com/term/per+share+rev/COIN/Revenue-per-Share/

    """
    revenue_url: str = f'https://www.gurufocus.com/term/revenue-per-share/{symbol}'
    revenue_soup: BeautifulSoup = get_html_soup(revenue_url)
    soup_items: ResultSet = revenue_soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not soup_items else soup_items[0].get('content')
    strlist: List[str] = content.split()
    short_strlist: List[str] = list(dropwhile(lambda x: x != 'is', strlist))    
    revenue_per_share: Optional[float] = None if len(short_strlist) < 3 else readf(short_strlist[1])
    return revenue_per_share




def proxy_guru_revenue(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
    DEPENDS: try_get_guru_revenue > get_guru_revenue
    
    """
    revenue_per_share: Optional[float] = get_guru_revenue_per_share(symbol)   
    proxy['revenue_per_share'] = revenue_per_share
    
    revenue_pc: Optional[float] = round((revenue_per_share / proxy['price'] * 100.0), 2) if (proxy.get('price') and revenue_per_share) else None
    proxy['revenue_pc'] = revenue_pc
    return proxy


def get_guru_revenue_growths(symbol: str) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float]]:
    """    
    returns Revenue Growths in years
    """
    revenue_url: str = f'https://www.gurufocus.com/term/revenue-per-share/{symbol}'
    html_text: str = get_html_text(revenue_url)
    # the + sign matches multiple occurrence of the same character, such as <<, >>, %%%, commonly use when there are spaces.
    # strlist is the result of spliting a whole page of html text.
    strlist: List[str] = re.split('[<>%]+', html_text)
    short_strlist: List[str] = list(dropwhile(lambda x: x != 'past 12 months', strlist))
    tiny_strlist: List[str] = short_strlist[:40]
    
    # growth strings of 1,3,5,10 years, some stocks such as COIN has fewer years of data.
    # filter out those words cannot be converted to numbers. 
    # growth_list (NVDA): ['11.70', '34.50', '25.70', '22.00']
    growth_list: list[str] = list(filter(lambda x: readf(x), tiny_strlist)) 
    rev_growth_1y: Optional[float] = None if len(growth_list) < 1 else readf(growth_list[0])
    rev_growth_3y: Optional[float] = None if len(growth_list) < 2 else readf(growth_list[1])
    rev_growth_5y: Optional[float] = None if len(growth_list) < 3 else readf(growth_list[2])
    rev_growth_10y: Optional[float] = None if len(growth_list) < 4 else readf(growth_list[3])

    return rev_growth_1y, rev_growth_3y, rev_growth_5y, rev_growth_10y




def proxy_guru_revenue_growths(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS: try_get_guru_revenue_growths"""
    rev_growth_1y, rev_growth_3y, rev_growth_5y, rev_growth_10y = get_guru_revenue_growths(symbol)
    proxy['rev_growth_1y'] = rev_growth_1y
    proxy['rev_growth_3y'] = rev_growth_3y
    proxy['rev_growth_5y'] = rev_growth_5y
    proxy['rev_growth_10y'] = rev_growth_10y
    return proxy





def get_guru_strength(symbol: str) -> Optional[float]:
    """
    https://www.gurufocus.com/term/rank-balancesheet/NVDA
    """
    strength_url: str = f'https://www.gurufocus.com/term/rank-balancesheet/{symbol}'
    strength_soup: BeautifulSoup = get_html_soup(strength_url)
    strength_soup_items: ResultSet = strength_soup.find_all('meta', attrs={'name': 'description'})
    content: str = '' if not strength_soup_items else strength_soup_items[0].get('content')

    strength_strlist: List[str] = content.split()
    strength_strlist_shortened: List[str] = list(dropwhile(lambda x: x != 'is', strength_strlist))    
    strength: Optional[float] = None if strength_strlist_shortened.__len__() < 3 else readf(strength_strlist_shortened[1])
    return strength






def proxy_guru_strength(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS: try_get_guru_strength > get_guru_strength"""
    strength: Optional[float] = get_guru_strength(symbol)
    proxy['strength'] = strength
    return proxy








def get_guru_zscore(symbol: str) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float]]:
    """

    https://www.gurufocus.com/term/zscore/NVDA

    https://www.gurufocus.com/term/zscore/WBD

    iloc first value -1 means the last row
    iloc second value -1 means the last column

    
    ALTERNATIVE: Use beautifulsoup to get zscore:

        zscore_soup: BeautifulSoup = get_html_soup(zscore_url)
        zscore_soup_items: ResultSet = zscore_soup.find_all('meta', attrs={'name': 'description'})
        content: str = '' if not zscore_soup_items else zscore_soup_items[0].get('content')
        strlist: List[str] = content.split()
        short_strlist: List[str] = list(dropwhile(lambda x: x != 'is', strlist))    
        zscore: Optional[float] = None if len(short_strlist) < 3 else readf(short_strlist[1])

        
    When Altman Z-Score is LESS THAN 1.8, it is in Distress Zones.
    When Altman Z-Score is between 1.8 and 3, it is in Grey Zones.
    When Altman Z-Score GREATER THAN 3, it is in Safe Zones.

    Morgan Stanley zscore is None, because guru website states that
    Altman Z-Score does not apply to banks and insurance companies.
        
    """
    zscore_url: str = f'https://www.gurufocus.com/term/zscore/{symbol}'
    
    dfs: List[DataFrame] = get_html_dataframes(zscore_url)
    
    not_valid: bool = len(dfs) < 8



    x1_str: Any = '' if len(dfs) < 3 or dfs[3].empty else dfs[3].iloc[-1, 2] 
    x1: Optional[float] = readf(x1_str)
    
    x2_str: Any = '' if len(dfs) < 3 or dfs[3].empty else dfs[4].iloc[-1, 2] 
    x2: Optional[float] = readf(x2_str)
    
    x3_str: Any = '' if len(dfs) < 3 or dfs[3].empty else dfs[5].iloc[-1, 2] 
    x3: Optional[float] = readf(x3_str)
    
    x4_str: Any = '' if len(dfs) < 3 or dfs[3].empty else dfs[6].iloc[-1, 2] 
    x4: Optional[float] = readf(x4_str)
    
    x5_str: Any = '' if len(dfs) < 3 or dfs[3].empty else dfs[7].iloc[-1, 2] 
    x5: Optional[float] = readf(x5_str)
    
    zscore_str: Any = '' if not_valid else dfs[2].iloc[-1, 2] 
    zscore: Optional[float] = readf(zscore_str)
        
    year1z_str: Any = '' if not_valid else dfs[0].iloc[-1, -1] 
    year1z: Optional[float] = readf(year1z_str)
    
    year2z_str: Any = '' if not_valid else dfs[0].iloc[-1, -2] 
    year2z: Optional[float] = readf(year2z_str)
    
    year3z_str: Any = '' if not_valid else dfs[0].iloc[-1, -3] 
    year3z: Optional[float] = readf(year3z_str)
    

    return x1, x2, x3, x4, x5, zscore, year1z, year2z, year3z





def proxy_guru_zscore(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """DEPENDS ON: get_guru_zscore"""
    x1, x2, x3, x4, x5, zscore, year1z, year2z, year3z = get_guru_zscore(symbol)

    z1 = round(x1 * 1.2, 2) if x1 else None
    z2 = round(x2 * 1.4, 2) if x2 else None
    z3 = round(x3 * 3.3, 2) if x3 else None
    z4 = round(x4 * 0.6, 2) if x4 else None
    z5 = round(x5 * 1.0, 2) if x5 else None

    nocapz = round(zscore - z4, 2)  if z4 and zscore else None

    proxy['x1'] = x1
    proxy['x2'] = x2
    proxy['x3'] = x3
    proxy['x4'] = x4
    proxy['x5'] = x5
    

    proxy['z1'] = z1
    proxy['z2'] = z2
    proxy['z3'] = z3
    proxy['z4'] = z4
    proxy['z5'] = z5

    proxy['zscore'] = zscore
    proxy['nocapz'] = nocapz

    proxy['year1z'] = year1z
    proxy['year2z'] = year2z
    proxy['year3z'] = year3z

    return proxy

















def gather_guru(SYMBOL: str) -> DictProxy:
    """
    DEPENDS: initialize_guru, proxy_guru_book_value() TO proxy_guru_zscore()
    
    """
    proxy: DictProxy = initialize_guru(SYMBOL)
    
    p1 = Process(target=proxy_guru_book_value, args=(SYMBOL, proxy))
    p2 = Process(target=proxy_guru_debt, args=(SYMBOL, proxy))
    p3 = Process(target=proxy_guru_earn, args=(SYMBOL, proxy))
    p4 = Process(target=proxy_guru_equity, args=(SYMBOL, proxy))
    p5 = Process(target=proxy_guru_interest, args=(SYMBOL, proxy))
    p6 = Process(target=proxy_guru_lynch, args=(SYMBOL, proxy))
    p7 = Process(target=proxy_guru_net_capital, args=(SYMBOL, proxy))
    p8 = Process(target=proxy_guru_net_margin, args=(SYMBOL, proxy))
    p9 = Process(target=proxy_guru_research, args=(SYMBOL, proxy))
    p10 = Process(target=proxy_guru_revenue, args=(SYMBOL, proxy))
    p11 = Process(target=proxy_guru_revenue_growths, args=(SYMBOL, proxy))
    p12 = Process(target=proxy_guru_strength, args=(SYMBOL, proxy))
    p13 = Process(target=proxy_guru_zscore, args=(SYMBOL, proxy))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()
    p9.start()
    p10.start()
    p11.start()
    p12.start()
    p13.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p8.join()
    p9.join()
    p10.join()
    p11.join()
    p12.join()
    p13.join()
    
    p1.close()
    p2.close()
    p3.close()
    p4.close()
    p5.close()
    p6.close()
    p7.close()
    p8.close()
    p9.close()
    p10.close()
    p11.close()
    p12.close()
    p13.close()
    return proxy


### END OF 2ND PHASE : GATHER_GURU ###







#################################
### 3RD PHASE : FINALIZE_GURU ###
#################################


def calculate_wealth_pc(proxy: DictProxy) -> Optional[float]:
    """
    wealth_pc is the sum of NET CAPITAL + TANGIBLE BOOK VALUE + NEXT 5 YEARS EARNINGS, in percentage of market capitalization.
    
    USED BY: make_guru_proxy
    """
    wealth_keys: List[str] = ['cap', 'price', 'earn_pc', 'net_capital_pc', 'book_value_pc']
    valid_keys: bool = all(key in proxy for key in wealth_keys)    
    valid_values: bool = all(value is not None for key, value in proxy.items() if key in wealth_keys) if valid_keys else False
    wealth_pc: Optional[float] = round((proxy['earn_pc'] * 5.0 + proxy['net_capital_pc'] + proxy['book_value_pc']), 2) if valid_values else None
    return wealth_pc


def finalize_guru(symbol: str) -> DictProxy:
    """
    DEPENDS: gather_guru(), get_guru_wealth_pc()
    """
    proxy: DictProxy = gather_guru(symbol)
    wealth_pc: Optional[float] = calculate_wealth_pc(proxy)
    proxy['wealth_pc'] = wealth_pc
    return proxy


### END OF 3RD PHASE : FINALIZE_GURU ###





#################################
### 4TH PHASE : UPSERT_GURU ###
#################################





def make_upsert_guru_cmd(proxy: DictProxy) -> str:
    
    table: str = 'guru_stock'
    
    columns: list[str] = list(proxy.keys())

    col_names: str = ', '.join(columns)

    placeholders: str = ', '.join(f'${i+1}' for i in range(len(columns)))

    update_cols: list[str] = [c for c in columns if c not in ('symbol',)]
    
    update_clause: str = ', '.join(f'{c} = EXCLUDED.{c}' for c in update_cols)

    query_cmd: str = f'''
        INSERT INTO {table} ({col_names})
        VALUES ({placeholders})
        ON CONFLICT (symbol) DO UPDATE SET {update_clause};
        '''
    return query_cmd



async def upsert_guru(symbol: str) -> None:
    """
    DEPENDS ON: finalize_guru, make_upsert_guru_cmd
    IMPORTS: make_guru_proxy()
    USED BY: upsert_gurus_by_terminal(), core_stock_update/core_update_controller.py
    I could wrap this function into try_str(upsert, symbol).
    """
    SYMBOL: str = symbol.upper()
    
    dict_proxy: DictProxy = finalize_guru(SYMBOL)
    
    valid_data: bool = dict_proxy.get('wealth_pc') is not None

    if valid_data:
        
        cmd: str = make_upsert_guru_cmd(dict_proxy)
        
        values = list(dict_proxy.values())
        
        print(dict_proxy)
 
        conn = await asyncpg.connect()
        
        result = await conn.execute(cmd, *values)                
        
        await conn.close()
        
        print(f'{SYMBOL} {dict_proxy} {result}')
    
    else:
        print(f'{symbol} {dict_proxy} DictProxy missed wealth_pc')





async def upsert_gurus(stock_list: list[str]) -> None:
    """
    DEPENDS:  upsert_gurus
    """
    length: int = len(stock_list)

    for i, symbol in enumerate(stock_list, start=1):
        try:
            await upsert_guru(symbol)

            output: str = f'SUCCESS {i} / {length} {symbol}'

            print(output)

        except Exception as e:
            error_output: str = f'ERROR {i} / {length} {symbol} {e}'
            print(error_output)





### END OF 4TH PHASE : UPSERT_GURU ###


if __name__ == '__main__':
    pass
    
    

