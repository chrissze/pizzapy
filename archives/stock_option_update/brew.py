
r"""
Q: HOW TO USE PYTHON TO EXTRACT ALL expirationDates below?

{"status":200,"statusText":"OK","headers":{},"body":"{\"optionChain\":{\"result\":[{\"underlyingSymbol\":\"NVDA\",\"expirationDates\":[1753401600,1754006400,1754611200,1755216000,1755820800,1756425600]  ...


"""

# STANDARD LIBS
from itertools import dropwhile

import json

from multiprocessing import Pool

from multiprocessing.managers import DictProxy

import os

import re

from typing import Any, List, Optional, Tuple, Union


# THIRD PARTY LIBS
from pandas import DataFrame
    
from bs4 import BeautifulSoup


# CUSTOM LIBS
from batterypy.string.read import float0

from dimsumpy.web.crawler import get_html_dataframes, get_html_text, get_selenium_text


# PROGRAM MODULES


def extract_unix_dates(symbol: str) -> List[str]:
    """
    IMPORTS: bs4, re, get_selenium_text()
    
    USED BY: prepare_urls()
    
    https://finance.yahoo.com/quote/NVDA/options

    Yahoo Finance website needs requests headers with Accept field.

    i. Get last unix timestamps from the browser by clicking on last year.
     
    ii. Search source code on that date, say 1829001600
     

    """

    url: str = f"https://finance.yahoo.com/quote/{symbol}/options"

    html_content = get_html_text(url)

    soup = BeautifulSoup(html_content, 'html.parser')


    # Find the script tag containing the expirationDates
    script_tags = soup.find_all("script")

    json_string = None
    
    for script in script_tags:
        if script.string and "expirationDates" in script.string:
            json_string = script.string
            break

    if not json_string:
        raise ValueError("Could not find script tag containing expirationDates")

    # Parse the JSON string

    converted_dict: dict = json.loads(json_string)

    body_dict: dict = json.loads(converted_dict.get('body'))
    
    date_list: list[str] = body_dict.get('optionChain').get('result')[0].get('expirationDates')




def test1() -> None:
    """
            https://finance.yahoo.com/quote/NVDA/options

    """
    xs = extract_unix_dates('QBTS')
    print(xs)


def test2() -> None:
    """
            https://finance.yahoo.com/quote/NVDA/options?date=1734652800

    """
    dfs = get_html_dataframes('https://finance.yahoo.com/quote/NVDA/options?date=1734652800')
    print(dfs)



def test3() -> None:
    
    
    p = proxy_option_money('NVDA', {'price': 140, 'cap': 3400000000000})

    print(p)



if __name__ == '__main__':
    test1()