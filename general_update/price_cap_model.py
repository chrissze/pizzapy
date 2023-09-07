
# STANDARD LIBRARIES
import sys; sys.path.append('..')
import json
from multiprocessing.managers import DictProxy
from typing import Any, Dict, List, Optional, Tuple


# THIRD PARTY LIBRARIES
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
import requests


# CUSTOM LIBRARIES
from batterypy.string.json import extract_nested_values
from batterypy.string.read import formatlarge, readf
from dimsumpy.web.crawler import get_html_soup


def get_barchart_price_cap(symbol: str) -> Tuple[Optional[float], Optional[float]] :
    """
    * INDEPENDENT *

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


def try_get_price_cap(symbol: str) -> Tuple[Optional[float], Optional[float]] :
    """
    DEPENDS ON: get_barchart_price_cap() 
    """
    try:
        price, cap = get_barchart_price_cap(symbol)
        return price, cap
    except requests.exceptions.RequestException as requests_error:
        print('try_get_barchart_price_cap RequestException: ', requests_error)
        return None, None
    except Exception as error:
        print('try_get_barchart_price_cap general Exception: ', error)
        return None, None


def proxy_price_cap(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
    DEPENDS ON: try_get_price_cap()
    I write `is not None` for testing below since price, cap might be 0, which is a false value.
    """
    price, cap = try_get_price_cap(symbol)    
    proxy['price'] = price if price is not None else None
    proxy['cap'] = cap if cap is not None else None
    proxy['capstr'] = formatlarge(cap) if cap is not None else None
    return proxy


if __name__ == '__main__':

    s = input('which str to you want to input? ')

    x = proxy_price_cap(s) 
    print(x)


    
