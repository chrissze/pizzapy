
# STANDARD LIBRARIES

from datetime import date, datetime
import json

from multiprocessing import Manager
from multiprocessing.managers import DictProxy, SyncManager

from typing import Any, Dict, List, Optional, Tuple


# THIRD PARTY LIBRARIES
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
import requests


# CUSTOM LIBRARIES
from batterypy.string.json import extract_nested_values
from batterypy.string.read import formatlarge, readf
from batterypy.time.cal import get_trading_day_utc
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


def make_price_cap_proxy(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
    DEPENDS ON: get_barchart_price_cap()
    I write `is not None` for testing below since price, cap might be 0, which is a false value.
    """
    price, cap = get_barchart_price_cap(symbol)    
    proxy['price'] = price
    proxy['cap'] = cap
    proxy['cap_str'] = formatlarge(cap) if cap is not None else None
    return proxy



def initialize_proxy(symbol: str) -> DictProxy:
    """
        * INDEPENDENT *
        IMPORTS: multiprocessing(DictProxy, SyncManager)
        USED BY: make_option_proxy()
    """
    manager: SyncManager = Manager()
    proxy: DictProxy = manager.dict()
    proxy['symbol'] = symbol
    proxy['td'] = get_trading_day_utc()
    proxy['t'] = datetime.now().replace(second=0, microsecond=0)
    return proxy



if __name__ == '__main__':

    s = input('which str to you want to input? ')

    x = make_price_cap_proxy(s) 
    print(x)


    
