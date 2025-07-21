
r"""


USED BY: option_proxy_model.py

        all_data_values = [tag['expirationDates'] for tag in soup.find_all(attrs={'expirationDates': True})]


        print(f"Extracted data values: {all_data_values}")

        unix_timestamp_pattern = re.compile(r'^\d{10,}$')

        filtered_unix_dates = [value for value in all_data_values if unix_timestamp_pattern.match(value)]

        return filtered_unix_dates
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




def calculate_premiums(call_df: DataFrame, put_df: DataFrame, price: Optional[float]) -> Tuple[float, float, float, float, float, float, float, float]:
    """
        * INDEPENDENT *
        USED BY: calculate_page_premiums()    
        call_premium and put_premium are already account for 100 shares multiplication.

        IsOTM column is originally Chg

        Use call_df.Chg and put_df.Chg as holders for Out of Money boolean
    """
    call_df.columns = ['Contract', 'LTD', 'Strike', 'Last', 'Bid',
                        'Ask', 'IsOTM', 'PercentChg', 'Volume', 'OI', 'Vol']
    put_df.columns = ['Contract', 'LTD', 'Strike', 'Last', 'Bid',
                        'Ask', 'IsOTM', 'PercentChg', 'Volume', 'OI', 'Vol']

    OTM = 0.0

    call_df.Last = [float0(x) for x in call_df.Last]    # convert Last price to float
    call_df.OI = [float0(x) for x in call_df.OI]        # convert open interest to float
    call_df.Vol = call_df.Last * call_df.OI             # Use Vol as a holder for money
    call_df.Strike = [float0(x) for x in call_df.Strike]        # convert strike to float
    call_df.IsOTM = call_df.Strike > price * (1 + OTM) if price else False   # Strike is 0 is still OK

    put_df.Last = [float0(x) for x in put_df.Last]
    put_df.OI = [float0(x) for x in put_df.OI]
    put_df.Vol = put_df.Last * put_df.OI
    put_df.Strike = [float0(x) for x in put_df.Strike]
    put_df.IsOTM = put_df.Strike < price * (1 - OTM) if price else False   

    call_premium: float = call_df.Vol.sum() * 100.0     # total call premium in that page
    put_premium: float = put_df.Vol.sum() * 100.0       # total put premium in that page

    call_otm_premium: float = call_df.loc[call_df['IsOTM'] == True, 'Vol'].sum() * 100
    call_itm_premium: float = call_df.loc[call_df['IsOTM'] == False, 'Vol'].sum() * 100
    put_otm_premium: float = put_df.loc[put_df['IsOTM'] == True, 'Vol'].sum() * 100
    put_itm_premium: float = put_df.loc[put_df['IsOTM'] == False, 'Vol'].sum() * 100
    call_open_interest: float = call_df.OI.sum()
    put_open_interest: float = put_df.OI.sum()
    return call_premium, put_premium, call_open_interest, put_open_interest, call_otm_premium, call_itm_premium, put_otm_premium, put_itm_premium
    

def calculate_page_premiums(xs: List[Any]) -> Tuple[float, float, float, float, float, float, float, float]:
    """
    DEPENDS ON: calculate_premiums()
    IMPORTS: get_html_dataframes(), pandas
    USED BY: get_total_premiums()

    
        https://finance.yahoo.com/quote/NVDA/options?date=1734652800

    """
    page = xs[0]
    
    price = xs[1]
    
    page_dfs: List[DataFrame] = get_html_dataframes(page)



    good_status: bool = len(page_dfs) > 1
    call_df: DataFrame = page_dfs[0] if good_status else DataFrame()
    put_df: DataFrame = page_dfs[1] if good_status else DataFrame()

    if len(call_df.columns) == 11 and len(put_df.columns) == 11:
        call_premium, put_premium, call_open_interest, put_open_interest, call_otm_premium, call_itm_premium, put_otm_premium, put_itm_premium = calculate_premiums(call_df, put_df, price)
    else:
        call_premium, put_premium, call_open_interest, put_open_interest, call_otm_premium, call_itm_premium, put_otm_premium, put_itm_premium = 0, 0, 0, 0, 0, 0, 0, 0  # default return values
    return call_premium, put_premium, call_open_interest, put_open_interest, call_otm_premium, call_itm_premium, put_otm_premium, put_itm_premium



def extract_unix_dates(symbol: str) -> list[str]:
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
    
    return date_list


def prepare_urls(symbol: str) -> List[str]:
    """

        DEPENDS ON: extract_unix_dates()

        USED BY: get_total_premiums()

        https://finance.yahoo.com/quote/NVDA/options

        https://finance.yahoo.com/quote/AMD/options/

        https://finance.yahoo.com/quote/NVDA/options?date=1734652800

        starting test this page
    """

    unix_dates: List[str] = extract_unix_dates(symbol)

    expiry_urls: List[str] = [f'https://finance.yahoo.com/quote/{symbol}/options?date={unix_date}' for unix_date in unix_dates]
    return expiry_urls



def get_total_premiums(price: Optional[float], symbol: str) -> Tuple[float, float, float, float, float, float, float, float]:
    """
        DEPENDS ON: calculate_page_premiums(), prepare_urls()
        IMPORTS: multiprocessing(Pool), os
        USED BY: proxy_option_money()
        
        This function runs in PARALLEL

        You don't need to use dill explicitly in your code, just importing it before using the pool.map method will make it the default serializer for the multiprocessing module. This will allow you to use lambda functions or other objects that are not serializable by pickle. You can learn more about how dill works from [this web page]. blush
    """

    urls: List[str] = prepare_urls(symbol)
    expiry_urls = [[url, price] for url in urls]

    cpu_count: int = min(os.cpu_count(), 8)                  
    with Pool(processes=cpu_count) as pool:
        result = pool.map(calculate_page_premiums, expiry_urls)
    
    call_money = sum(call_premium for call_premium, _, _, _,            _, _, _, _ in result)
    put_money = sum(put_premium for _, put_premium, _, _,               _, _, _, _ in result) 
    call_oi = sum(call_open_interest for _, _, call_open_interest, _,   _, _, _, _ in result)
    put_oi = sum(put_open_interest for _, _, _, put_open_interest,      _, _, _, _ in result)

    call_otm = sum(call_otm_premium for _, _, _, _,                     call_otm_premium, _, _, _ in result)
    call_itm = sum(call_itm_premium for _, _, _, _,                     _, call_itm_premium, _, _ in result)
    put_otm = sum(put_otm_premium for _, _, _, _,                       _, _, put_otm_premium, _ in result)
    put_itm = sum(put_itm_premium for _, _, _, _,                       _, _, _, put_itm_premium in result)

    return call_money, put_money, call_oi, put_oi, call_otm, call_itm, put_otm, put_itm



def proxy_option_money(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
        DEPENDS ON: get_total_premiums()

        USED BY: make_option_proxy()
        
        Optionally rely on make_price_cap_proxy() to create a DictProxy in make_option_proxy()

        Hypothesis:
            If OTM put option has a higher ratio, the stock is like to fall further.
    """
    price: Optional[float] = proxy.get('price')

    call_money, put_money, call_oi, put_oi, call_otm, call_itm, put_otm, put_itm = get_total_premiums(price, symbol)
    
    total_money: Optional[float] = call_money + put_money if call_money > 0 and put_money > 0 else None

    call_ratio: Optional[float] = round((call_money / total_money * 100.0), 1) if total_money is not None else None
    put_ratio: Optional[float] = round((put_money / total_money * 100.0), 1) if total_money is not None else None

    call_pc: Optional[float] = round((call_money / proxy['cap'] * 100.0), 4) if (call_money > 0 and proxy.get('cap')) else None
    put_pc: Optional[float] = round((put_money / proxy['cap'] * 100.0), 4) if (put_money > 0 and proxy.get('cap')) else None
    

    call_otm_ratio: Optional[float] = round((call_otm / call_money * 100.0), 1) if call_otm and call_money else None
    call_itm_ratio: Optional[float] = round((call_itm / call_money * 100.0), 1) if call_itm and call_money else None
    put_otm_ratio: Optional[float] = round((put_otm / put_money * 100.0), 1) if put_otm and put_money else None
    put_itm_ratio: Optional[float] = round((put_itm / put_money * 100.0), 1) if put_itm and put_money else None


    proxy['call_money'] = round(call_money, 0) if call_money > 0 else None
    proxy['put_money'] = round(put_money, 0) if put_money > 0 else None
    proxy['call_oi'] = round(call_oi, 0) if call_oi > 0 else None
    proxy['put_oi'] = round(put_oi, 0) if put_oi > 0 else None
    proxy['call_ratio'] = call_ratio
    proxy['put_ratio'] = put_ratio

    proxy['call_otm_ratio'] = call_otm_ratio
    proxy['call_itm_ratio'] = call_itm_ratio
    proxy['put_otm_ratio'] = put_otm_ratio
    proxy['put_itm_ratio'] = put_itm_ratio

    proxy['call_pc'] = call_pc
    proxy['put_pc'] = put_pc

    return proxy




def test1() -> None:
    """
            https://finance.yahoo.com/quote/NVDA/options

    """
    xs = extract_unix_dates('NVDA')
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
    test3()