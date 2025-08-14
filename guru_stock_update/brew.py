
# STANDARD LIBRARIES

import json
from multiprocessing.managers import DictProxy
from typing import Any, Dict, List, Optional, Tuple


# THIRD PARTY LIBRARIES

from bs4 import BeautifulSoup
from bs4.element import ResultSet

from pandas.core.frame import DataFrame

import requests


# CUSTOM LIBRARIES
from batterypy.string.read import readf
from dimsumpy.web.crawler import get_html_soup

# PROGRAM MODULES
from pizzapy.general_update.general_model import make_price_cap_proxy




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
    
    #print(f'{content=}')
    #print(f'{strlist2=}')
    #print(f'{payout_yield=}')
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




def get_share_change(symbol: str, d: DictProxy={}) -> Optional[float]:
    """
    REQUIRES: 

    https://macrotrends.net/stocks/charts/NVDA/x/shares-outstanding

    share_change_url: str = f'https://macrotrends.net/stocks/charts/{symbol}/x/shares-outstanding'
    soup: BeautifulSoup = get_html_soup(share_change_url)
    
    soup_items: ResultSet = soup.find('meta', attrs={'name': 'description'})
    
    content: str = '' if not soup_items else soup_items.get('content')

    strlist: List[str] = content.split()

    strlist2: List[str] = list(filter(lambda x: '%' in x, strlist))

    share_change: Optional[float] = readf(strlist2[0][:-1]) if strlist2 else None
    
    print(f'{soup_items=}')
    print(f'{content=}')
    print(f'{strlist=}')
    print(f'{strlist2=}')
    print(f'{share_change=}')
    return share_change
    """


    url = "https://m.macrotrends.net/stocks/charts/NVDA/nvidia/shares-outstanding"
    headers = {'User-Agent': 'Mozilla/5.0'}  # Simulate a browser request

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    meta_description = soup.find('meta', attrs={'name': 'description'})
    if meta_description:
        print(meta_description.get('content'))
    else:
        print("Meta description not found.")




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
    proxy['share_change'] = get_share_change(symbol)
    return proxy




def test():
    
    stock = input('which stock do you want to check? ')
    proxy = make_price_cap_proxy(stock)
    x = proxy_guru_earn(stock, proxy=proxy)
    print(x)
    

def test1():
    get_share_change('NVDA')

if __name__ == '__main__':
    
    test1()