"""

"""
# STANDARD LIBS

from datetime import date, datetime
from multiprocessing.managers import DictProxy
from typing import Any, List, Optional, Tuple, Union


# THIRD PARTY LIBS

from pandas import DataFrame

# CUSTOM LIBS
from batterypy.string.read import readf
# PROGRAM MODULES
from dimsumpy.web.crawler import get_html_dataframes





def get_zacks_industry(symbol: str) -> Tuple[Optional[date], Optional[float], Optional[float], Optional[float], Optional[float]]:
    """
    DEPENDS ON: get_earning_date()
    IMPORTS: dimsumpy(get_html_dataframes), batterypy(readf)
    USED BY: proxy_zacks_earings()

    https://www.zacks.com/stock/research/NVDA/industry-comparison

    Need to Use US VPN
    """

    url: str = f'https://www.zacks.com/stock/research/{symbol}/industry-comparison'
    dfs: List[DataFrame] = get_html_dataframes(url)
    low_frames: bool = len(dfs) < 6

    #print(len(dfs))
    
    pe_str: str = '' if low_frames else dfs[5].iloc[0, 1]
    pe: Optional[float] = readf(pe_str)
    
    pbook_str: str = '' if low_frames else dfs[5].iloc[1, 1]
    pbook: Optional[float] = readf(pbook_str)
    
    pcashflow_str: str = '' if low_frames else dfs[5].iloc[2, 1]
    pcashflow: Optional[float] = readf(pcashflow_str)

    profit_margin_str: str = '' if low_frames else dfs[5].iloc[4, 1]
    profit_margin: Optional[float] = readf(profit_margin_str)

    return pe, pbook, pcashflow, profit_margin




def proxy_zacks_industry(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
    DEPENDS ON: get_zacks_earings()
    
    USED BY: zacks_proxy_model.py

    """
    pe, pbook, pcashflow, profit_margin = get_zacks_industry(symbol)
    proxy['next_earning_date'] = next_earning_date
    proxy['broker_rating'] = broker_rating
    proxy['eps'] = eps
    proxy['forward_eps'] = forward_eps
    proxy['diluted_eps_ttm'] = diluted_eps_ttm
    return proxy


# def full_test() -> None:
#     symbol: str = input('What SYMBOL do you want to check? ')
#     x = proxy_zacks_earnings(symbol)
#     print(x)




def test() -> None:
    symbol: str = input('What SYMBOL do you want to check? ')
    x = get_zacks_industry(symbol)
    print(x)

if __name__ == '__main__':
    test()
