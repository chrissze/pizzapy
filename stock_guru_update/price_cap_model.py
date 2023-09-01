
# STANDARD LIBRARIES
import sys; sys.path.append('..')
import json
from multiprocessing.managers import DictProxy
from timeit import default_timer
from typing import Any, Dict, List, Optional, Tuple


# THIRD PARTY LIBRARIES
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
import pandas
from pandas.core.frame import DataFrame
import requests
from requests.models import Response


# CUSTOM LIBRARIES
from batterypy.string.json import extract_nested_values
from batterypy.string.read import formatlarge, readf


safari_headers: Dict[str, str] = {'User-Agent': 'Safari/13.1.1'}

def get_html_text(url: str) -> str :
    ''' INDEPENDENT
    requires: requests
    '''
    html_response: Response = requests.get(url, headers=safari_headers)
    return html_response.text


def get_html_soup(url: str) -> BeautifulSoup :
    ''' 
    depends: get_html_text
    requires: beautifulsoup4
    '''
    html_text: str = get_html_text(url)
    soup: BeautifulSoup = BeautifulSoup(html_text, 'html.parser')
    return soup


def get_html_dataframes(url: str) -> List[DataFrame]:
    '''INDEPENDENT
    requires: beautifulsoup4, pandas, requests

    https://google.com   (has <table>)
    https://yahoo.com   (no <table>)
    https://googel.com   (INVALID SSL cert)

    If there is non <table> tag, soup_tables will be just be empty ResultRet [], soup.find_all() function is safe.
    
    I MUST ensure html_text has a <table> tag, otherwise pandas.read_html will have No tables found error.
    '''
    html_text: str = get_html_text(url)
    soup: BeautifulSoup = BeautifulSoup(html_text, 'html.parser')
    soup_tables: ResultSet = soup.find_all('table')
    dataframes: List[DataFrame] = pandas.read_html(html_text, header=0) if soup_tables else []
    return dataframes


def get_barchart_price_cap(symbol: str) -> Tuple[Optional[float], Optional[float]] :
    '''DEPENDS: get_html_soup

    requires standard libs: json
    requires 3rd party libs: beautifulsoup4
    requires custom libs: batterypy
        
    I can use this function to display the marketcap dictionary in formatted string:
        json_cap_pretty: str = json.dumps(json_cap, indent=2)

    '''
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


def tryget_price_cap(symbol: str) -> Tuple[Optional[float], Optional[float]] :
    '''DEPENDS: get_barchart_price_cap '''
    try:
        price, cap = get_barchart_price_cap(symbol)
        return price, cap
    except requests.exceptions.RequestException as requests_error:
        print('tryget_barchart_price_cap RequestException: ', requests_error)
        return None, None
    except Exception as error:
        print('tryget_barchart_price_cap general Exception: ', error)
        return None, None


def proxy_price_cap(symbol: str, proxy: DictProxy={}) -> DictProxy:
    '''
    DEPENDS: tryget_price_cap > get_barchart_price_cap
    I write is not None for testing below since price, cap might be 0, which is a false value.
    '''
    price, cap = tryget_price_cap(symbol)    
    proxy['price'] = price if price is not None else None
    proxy['cap'] = cap if cap is not None else None
    proxy['capstr'] = formatlarge(cap) if cap is not None else None
    return proxy


if __name__ == '__main__':

    s = input('which str to you want to input? ')

    x = proxy_price_cap(s) 
    print(x)


    
