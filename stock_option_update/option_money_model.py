

# STANDARD LIBS
import sys; sys.path.append('..')
from datetime import datetime
from itertools import dropwhile

from multiprocessing import Manager, Pool, Process
from multiprocessing.managers import DictProxy, SyncManager

import os
from typing import Any, List, Optional, Tuple, Union


# THIRD PARTY LIBS
from pandas import DataFrame


# CUSTOM LIBS
from batterypy.string.read import float0

from dimsumpy.web.crawler import get_html_dataframes, get_html_text



# PROGRAM MODULES




def calculate_premiums(call_df: DataFrame, put_df: DataFrame) -> Tuple[float, float, float, float]:
    """
        * INDEPENDENT *
        USED BY: calculate_page_premiums()    
        call_premium and put_premium are already account for 100 shares multiplication.
    """
    call_df.columns = ['Contract', 'LTD', 'Strike', 'Last', 'Bid',
                        'Ask', 'Chg', 'PercentChg', 'Volume', 'OI', 'Vol']
    put_df.columns = ['Contract', 'LTD', 'Strike', 'Last', 'Bid',
                        'Ask', 'Chg', 'PercentChg', 'Volume', 'OI', 'Vol']

    call_df.Last = [float0(x) for x in call_df.Last]
    call_df.OI = [float0(x) for x in call_df.OI]
    call_df.Vol = call_df.Last * call_df.OI

    put_df.Last = [float0(x) for x in put_df.Last]
    put_df.OI = [float0(x) for x in put_df.OI]
    put_df.Vol = put_df.Last * put_df.OI

    call_premium: float = call_df.Vol.sum() * 100.0
    put_premium: float = put_df.Vol.sum() * 100.0
    call_open_interest: float = call_df.OI.sum()
    put_open_interest: float = put_df.OI.sum()
    return call_premium, put_premium, call_open_interest, put_open_interest
    

def calculate_page_premiums(page: str) -> Tuple[float, float, float, float]:
    """
    DEPENDS ON: calculate_premiums()
    IMPORTS: get_html_dataframes(), pandas
    USED BY: get_total_premiums()
    https://finance.yahoo.com/quote/AMD/options?date=1695945600
    """
    page_dfs: List[DataFrame] = get_html_dataframes(page)
    good_status: bool = len(page_dfs) > 1
    call_df: DataFrame = page_dfs[0] if good_status else DataFrame()
    put_df: DataFrame = page_dfs[1] if good_status else DataFrame()

    if len(call_df.columns) == 11 and len(put_df.columns) == 11:
        call_premium, put_premium, call_open_interest, put_open_interest = calculate_premiums(call_df, put_df)
    else:
        call_premium, put_premium, call_open_interest, put_open_interest = 0.0, 0.0, 0.0, 0.0  # default return values
    return call_premium, put_premium, call_open_interest, put_open_interest



def prepare_urls(symbol: str) -> List[str]:
    """
        IMPORTS: get_html_text()
        USED BY: get_total_premiums()
    """
    option_url: str = f"https://finance.yahoo.com/quote/{symbol}/options"
    html_text: str = get_html_text(option_url)
    raw_string_list: List[str] = html_text.split('"')
    short_string_list: List[str] = list(dropwhile(lambda s: s != 'expirationDates', raw_string_list))
    dates_str: str = short_string_list[1][2:-2] if len(short_string_list) > 1 else ''
    unix_dates: List[str] = dates_str.split(',')
    expiry_urls: List[str] = [f'https://finance.yahoo.com/quote/{symbol}/options?date={unix_date}' for unix_date in unix_dates]
    return expiry_urls


def get_total_premiums(symbol: str) -> Tuple[float, float, float, float]:
    """
        DEPENDS ON: calculate_page_premiums(), prepare_urls()
        IMPORTS: multiprocessing(Pool), os
        USED BY: proxy_option_money()
        
        This function runs in PARALLEL
    """
    expiry_urls = prepare_urls(symbol)
    cpu_count: int = min(os.cpu_count(), 8)                  
    with Pool(processes=cpu_count) as pool:
        result = pool.map(calculate_page_premiums, expiry_urls)
    
    call_money = sum(call_premium for call_premium, _, _, _ in result)
    put_money = sum(put_premium for _, put_premium, _, _ in result) 
    call_oi = sum(call_open_interest for _, _, call_open_interest, _ in result)
    put_oi = sum(put_open_interest for _, _, _, put_open_interest in result)

    return call_money, put_money, call_oi, put_oi



def proxy_option_money(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
        DEPENDS ON: get_total_premiums()
        USED BY: make_option_proxy()
        Optionally rely on make_price_cap_proxy() to create a DictProxy in make_option_proxy()
    """
    call_money, put_money, call_oi, put_oi = get_total_premiums(symbol)
    
    total_money: Optional[float] = call_money + put_money if call_money > 0 and put_money > 0 else None

    call_ratio: Optional[float] = round((call_money / total_money * 100.0), 1) if total_money is not None else None
    put_ratio: Optional[float] = round((put_money / total_money * 100.0), 1) if total_money is not None else None

    call_pc: Optional[float] = round((call_money / proxy['cap'] * 100.0), 4) if (call_money > 0 and proxy.get('cap')) else None
    put_pc: Optional[float] = round((put_money / proxy['cap'] * 100.0), 4) if (put_money > 0 and proxy.get('cap')) else None
    
    proxy['call_money'] = round(call_money, 0) if call_money > 0 else None
    proxy['put_money'] = round(put_money, 0) if put_money > 0 else None
    proxy['call_oi'] = round(call_oi, 0) if call_oi > 0 else None
    proxy['put_oi'] = round(put_oi, 0) if put_oi > 0 else None
    proxy['call_ratio'] = call_ratio
    proxy['put_ratio'] = put_ratio
    proxy['call_pc'] = call_pc
    proxy['put_pc'] = put_pc

    return proxy




def test() -> None:
    symbol = input('What SYMBOL do you want to input? ')
    
    option_proxy: DictProxy = proxy_option_money(symbol)
    print(option_proxy)    



if __name__ == '__main__':
    test()