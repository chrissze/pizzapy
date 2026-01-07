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



def get_next_earning_date(dfs: List[DataFrame]) -> Optional[date]:
    """
    * INDEPENDENT *
    USED BY: get_zacks_earnings()
    
    'USO' type is float
    """
    
    earning_date_str: Any = '' if len(dfs) < 11 else dfs[2].iloc[0, -1]


    earning_date_invalid: bool = (not isinstance(earning_date_str, str)) or '/' not in earning_date_str  
    earning_date: Optional[date] = None if earning_date_invalid else datetime.strptime(earning_date_str.replace('*AMC','').replace('*BMO',''), '%m/%d/%y').date()
    return earning_date



def get_zacks_earnings(symbol: str) -> Tuple[Optional[date], Optional[float], Optional[float], Optional[float], Optional[float]]:
    """
    DEPENDS ON: get_earning_date()
    IMPORTS: dimsumpy(get_html_dataframes), batterypy(readf)
    USED BY: proxy_zacks_earings()

    eps_ttm is the DILUTED eps for the past 12 months.

    broker_rating scale is 1 to 5: 1 is strong buy, 5 is strong sell

    https://www.zacks.com/stock/quote/NVDA/detailed-earning-estimates

    Need to Use US VPN
    """

    url: str = f'https://www.zacks.com/stock/quote/{symbol}/detailed-earning-estimates'
    dfs: List[DataFrame] = get_html_dataframes(url)
    low_frames: bool = len(dfs) < 11

    #print(dfs)

    next_earning_date: Optional[date] = get_next_earning_date(dfs)

    broker_rating_str: str = '' if low_frames else dfs[2].iloc[-1, -1]
    broker_rating: Optional[float] = readf(broker_rating_str)

    eps_str: str = '' if low_frames else dfs[3].iloc[1, -1]
    eps: Optional[float] = readf(eps_str)

    forward_eps_str: str = '' if low_frames else dfs[3].iloc[2,-1]
    forward_eps: Optional[float] = readf(forward_eps_str)

    diluted_eps_ttm_str: str = '' if low_frames else dfs[3].iloc[3,-1]
    diluted_eps_ttm: Optional[float] = readf(diluted_eps_ttm_str)
    

    return next_earning_date, broker_rating, eps, forward_eps, diluted_eps_ttm




def proxy_zacks_earnings(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
    DEPENDS ON: get_zacks_earings()
    
    USED BY: zacks_proxy_model.py

    """
    next_earning_date, broker_rating, eps, forward_eps, diluted_eps_ttm = get_zacks_earnings(symbol)
    proxy['next_earning_date'] = next_earning_date
    proxy['broker_rating'] = broker_rating
    proxy['eps'] = eps
    proxy['forward_eps'] = forward_eps
    proxy['diluted_eps_ttm'] = diluted_eps_ttm
    return proxy


def full_test() -> None:
    symbol: str = input('What SYMBOL do you want to check? ')
    x = proxy_zacks_earnings(symbol)
    print(x)




def test() -> None:
    symbol: str = input('What SYMBOL do you want to check? ')
    x = get_zacks_earnings(symbol)
    print(x)

if __name__ == '__main__':
    full_test()
