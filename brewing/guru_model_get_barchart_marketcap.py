
# STANDARD LIBRARIES
import sys; sys.path.append('..')

import json

from multiprocessing.managers import DictProxy
from timeit import default_timer
from typing import Any, Dict, List, Optional, Tuple, Union


# THIRD PARTY LIBRARIES
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.series import Series

import requests
from requests.models import Response


# CUSTOM LIBRARIES
from batterypy.string.json import extract_nested_values
from batterypy.string.read import formatlarge, is_floatable, readf, readi, readlarge

# PROJECT MODULES







# from itertools import dropwhile, takewhile
# 
# from multiprocessing import Manager, Process
# from datetime import datetime
# from urllib.request import Request, urlopen



# from numpy import float64



# import re

# from PySide2.QtWidgets import (QApplication, QTableView, QVBoxLayout ,QWidget)

# from dimsumpy.database.postgres import upsertquery, upsert_dict
# from dimsumpy.qt5.dataframemodel import DataFrameModel

# from batterypy.time.cal import get_trading_day, get_trading_day_utc



# from shared_model.sql_model import cnx, db_dict  # the postgres server must running
# from shared_model.st_data_model import stock_list_dict



def get_barchart_marketcap(symbol: str, d: DictProxy={}) -> Tuple[Optional[float], Optional[float]] :
    '''
    requires standard libs: json, multiprocessing, typing
    requires 3rd party libs: beautifulsoup4, pandas, requests,
    requires custom libs: batterypy
        
    I can use this function to display the marketcap dictionary in formatted string:
        json_cap_pretty: str = json.dumps(json_cap, indent=2)

    '''
    headers: Dict[str, str] = {'User-Agent': 'Safari/13.1.1'}
    try:
        url: str = "https://www.barchart.com/stocks/quotes/" + symbol
        html_response: Response = requests.get(url, headers=headers)
        soup: BeautifulSoup = BeautifulSoup(html_response.text, 'html.parser')
        soup_items: ResultSet = soup.find('div', attrs={'data-ng-controller': 'symbolHeaderCtrl'})
        item: str = soup_items.get('data-ng-init')

        json_price: Dict[str, Any] = json.loads(item[5:-1])

        price: Optional[float] = readf(json_price.get('lastPrice'))
        if price is not None:
            d['price'] = price
        
        cap_soup_items: ResultSet = soup.find('script', id='bc-dynamic-config')
        json_cap: Dict[str, Any] = json.loads(cap_soup_items.string)
        
        marketcaps: List[Any] = extract_nested_values(json_cap, 'marketCap')
        cap: Optional[float] = None if len(marketcaps) < 3 else readf(marketcaps[2])

        if cap is not None:
            d['cap'] = cap
            d['capstr']: str = formatlarge(cap)
            print(price, cap, d['capstr'])
        return price, cap
        

    except requests.exceptions.RequestException as requests_error:
        print('bar_cap RequestException: ', requests_error)
        return None, None
    except Exception as error:
        print('bar_cap Exception: ', error)
        return None, None



if __name__ == '__main__':
    start: float = default_timer()
    
    stock = input('which stock do you want to check? ')
    get_barchart_marketcap(stock)
    
    print('elapsed time in seconds:', default_timer() - start)
    
