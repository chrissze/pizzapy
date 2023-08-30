
# STANDARD LIBRARIES
import sys; sys.path.append('..')
import json
from multiprocessing.managers import DictProxy
from timeit import default_timer
from typing import Any, Dict, List, Optional, Tuple


# THIRD PARTY LIBRARIES
from bs4 import BeautifulSoup
from bs4.element import ResultSet
import pandas
from pandas.core.frame import DataFrame
import requests
from requests.models import Response


# CUSTOM LIBRARIES
from batterypy.string.json import extract_nested_values
from batterypy.string.read import formatlarge, readf


safari_headers: Dict[str, str] = {'User-Agent': 'Safari/13.1.1'}

def get_html_soup(url: str) -> BeautifulSoup :
    ''' INDEPENDENT
    requires: beautifulsoup4, requests
    '''
    html_response: Response = requests.get(url, headers=safari_headers)
    soup: BeautifulSoup = BeautifulSoup(html_response.text, 'html.parser')
    return soup


def get_html_dataframes(url: str) -> List[DataFrame]:
    '''INDEPENDENT
    requires: beautifulsoup4, pandas, requests
    '''
    html_response: Response = requests.get(url, headers=safari_headers)
    soup: BeautifulSoup = BeautifulSoup(html_response.text, 'html.parser')
    soup_tables: ResultSet = soup.find_all('table')
    no_table: bool = len(soup_tables) == 0
    dataframes: List[DataFrame] = [] if no_table else pandas.read_html(html_response.text, header=0)
    return dataframes



def get_barchart_price_cap(symbol: str) -> Tuple[Optional[float], Optional[float]] :
    '''DEPENDS: get_html_soup

    requires standard libs: json
    requires 3rd party libs: beautifulsoup4
    requires custom libs: batterypy
        
    I can use this function to display the marketcap dictionary in formatted string:
        json_cap_pretty: str = json.dumps(json_cap, indent=2)

    '''
    barchart_quotes_url: str = f'https://www.barchart.com/stocks/quotes/{symbol}'
    soup = get_html_soup(barchart_quotes_url)
    soup_items: ResultSet = soup.find('div', attrs={'data-ng-controller': 'symbolHeaderCtrl'})
    item: str = soup_items.get('data-ng-init')
    json_price: Dict[str, Any] = json.loads(item[5:-1])
    price: Optional[float] = readf(json_price.get('lastPrice'))
    
    cap_soup_items: ResultSet = soup.find('script', id='bc-dynamic-config')
    json_cap: Dict[str, Any] = json.loads(cap_soup_items.string)
    marketcaps: List[Any] = extract_nested_values(json_cap, 'marketCap')
    cap: Optional[float] = None if len(marketcaps) < 3 else readf(marketcaps[2])
    return price, cap


def tryget_price_cap(symbol: str) -> Tuple[Optional[float], Optional[float]] :
    '''DEPENDS: get_barchart_price_cap '''
    try:
        return get_barchart_price_cap(symbol)
    except requests.exceptions.RequestException as requests_error:
        print('tryget_barchart_price_cap RequestException: ', requests_error)
        return None, None
    except Exception as error:
        print('tryget_barchart_price_cap general Exception: ', error)
        return None, None


def proxy_price_cap(symbol: str, d: DictProxy={}) -> DictProxy:
    '''DEPENDS: tryget_price_cap > get_barchart_price_cap'''
    price, cap = tryget_price_cap(symbol)
    if price is not None:
        d['price'] = price
    
    if cap is not None:
        d['cap'] = cap
        d['capstr']: str = formatlarge(cap)
    return d


if __name__ == '__main__':
    start: float = default_timer()
    
    stock = input('which stock do you want to check? ')
    proxy = proxy_price_cap(stock)
    print(proxy)
    print('elapsed time in seconds:', default_timer() - start)
    
