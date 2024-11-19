"""

profit_margin also appears on Zacks' Comparison to Industry page.

"""
# STANDARD LIBS

from datetime import date, datetime


from multiprocessing.managers import DictProxy, SyncManager
from multiprocessing import Manager, Process
from timeit import default_timer
from typing import Any, List, Optional, Tuple, Union


# THIRD PARTY LIBS

import pandas
from pandas.core.frame import DataFrame
from pandas.core.series import Series

import requests
from requests.models import Response
from requests.structures import CaseInsensitiveDict



# CUSTOM LIBS
from batterypy.string.read import readf, readi
from batterypy.time.cal import get_trading_day, get_trading_day_utc

# PROGRAM MODULES
from dimsumpy.web.crawler import get_html_dataframes, get_html_text



def get_grades(dfs: List[DataFrame]) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    * INDEPENDENT - helper of get_zacks_scores()*

    USED BY: get_zacks_scores()

    input dfs is from get_zacks_scores().

    Value Growth Momentum, grading A B C D F
    averge_grade is the average of Value, Growth and Momentum
    """
    low_frames: bool = len(dfs) < 12

    vgm_str: str = '' if low_frames else dfs[4].iloc[8, 1]
    vgm_invalid: bool = (not isinstance(vgm_str, str)) or len(vgm_str) != 1
    average_grade: Optional[str] = None if vgm_invalid else vgm_str

    value_str: str = '' if low_frames else dfs[2].columns[1][0][-1]
    value_grade: Optional[str] = None if not value_str else value_str

    growth_str: str = '' if low_frames else dfs[4].columns[1][0][-1]
    growth_grade: Optional[str] = None if not growth_str else growth_str

    momentum_str: str = '' if low_frames else dfs[6].columns[1][0][-1]
    momentum_grade: Optional[str] = None if not momentum_str else momentum_str
    return average_grade, value_grade, growth_grade, momentum_grade



def get_profits(df: DataFrame) -> Optional[float]:
    """
    IMPORTS: batterypy(readf)
    USED BY: get_zacks_scores()

    helper of get_zacks_scores()
    input dfs is from get_zacks_scores().
    """
    low_rows: bool = len(df) < 15

    profit_margin_str: str = '' if low_rows else df.iloc[15, 1]
    profit_margin: Optional[float] = readf(profit_margin_str)
    return profit_margin


def get_price_ratios(dfs: List[DataFrame]) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float]]:
    """
    IMPORTS: batterypy(readf)
    USED BY: get_zacks_scores()

    helper of get_zacks_scores()
    input dfs is from get_zacks_scores().
    """
    low_frames: bool = len(dfs) < 12

    pe_str: str = '' if low_frames else dfs[2].iloc[14, 1]
    pe: Optional[float] = readf(pe_str)

    earning_yield_str: str = '' if low_frames else dfs[2].iloc[16, 1]
    earning_yield: Optional[float] = readf(earning_yield_str)

    pe_growth_ratio_str: Any = '' if low_frames else dfs[2].iloc[11, 1]
    pe_growth_ratio: Optional[float] = readf(pe_growth_ratio_str)

    psales_str: str = '' if low_frames else dfs[2].iloc[15, 1]
    psales: Optional[float] = readf(psales_str)

    pbook_str: str = '' if low_frames else dfs[2].iloc[12, 1]
    pbook: Optional[float] = readf(pbook_str)

    pcashflow_str: str = '' if low_frames else dfs[2].iloc[13, 1]
    pcashflow: Optional[float] = readf(pcashflow_str)

    cash_pc_str: str = '' if low_frames else dfs[2].iloc[9, 1]
    cash_pc: Optional[float] = readf(cash_pc_str)
    return pe, earning_yield, pe_growth_ratio, psales, pbook, pcashflow, cash_pc



def get_changes(df: DataFrame) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float], Optional[float]]:
    """
    IMPORTS: batterypy(readf)
    USED BY: get_zacks_scores()
    
    helper of get_zacks_scores()
    input dfs is from get_zacks_scores().

    """
    low_rows: bool = len(df) < 13

    chg_1d_str: str = '' if low_rows else df.iloc[9, 1]
    chg_1d: Optional[float] = readf(chg_1d_str[:-1])

    chg_5d_str: str = '' if low_rows else df.iloc[10, 1]
    chg_5d: Optional[float] = readf(chg_5d_str[:-1])

    chg_1m_str: str = '' if low_rows else df.iloc[11, 1]
    chg_1m: Optional[float] = readf(chg_1m_str[:-1])

    chg_3m_str: str = '' if low_rows else df.iloc[12, 1]
    chg_3m: Optional[float] = readf(chg_3m_str[:-1])

    chg_1y_str: str = '' if low_rows else df.iloc[13, 1]
    chg_1y: Optional[float] = readf(chg_1y_str[:-1])
    return chg_1d, chg_5d, chg_1m, chg_3m, chg_1y



def get_zacks_scores(symbol: str) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float]]:
    """
    DEPENDS ON: get_grades(), get_price_ratios(), get_changes()

    IMPORTS: dimsumpy(get_html_dataframes)
    
    USED BY: proxy_zacks_scores()

    https://www.zacks.com/stock/research/NVDA/stock-style-scores
    https://www.zacks.com/stock/research/INTC/stock-style-scores
    """

    url: str = f'https://www.zacks.com/stock/research/{symbol}/stock-style-scores'
    dfs: List[DataFrame] = get_html_dataframes(url)

    average_grade, value_grade, growth_grade, momentum_grade = get_grades(dfs)
    pe, earning_yield, pe_growth_ratio, psales, pbook, pcashflow, cash_pc = get_price_ratios(dfs)
    profit_margin = get_profits(dfs[4])
    chg_1d, chg_5d, chg_1m, chg_3m, chg_1y = get_changes(dfs[6])

    return average_grade, value_grade, growth_grade, momentum_grade, \
           pe, earning_yield, pe_growth_ratio, psales, pbook, pcashflow, cash_pc, \
           profit_margin, \
           chg_1d, chg_5d, chg_1m, chg_3m, chg_1y




def proxy_zacks_scores(symbol: str, proxy: DictProxy={}) -> DictProxy:
    """
    DEPENDS ON: get_zacks_scores()

    USED BY: zacks_proxy_model.py
    """
    average_grade, value_grade, growth_grade, momentum_grade, \
        pe, earning_yield, pe_growth_ratio, psales, pbook, pcashflow, cash_pc, \
        profit_margin, \
        chg_1d, chg_5d, chg_1m, chg_3m, chg_1y = get_zacks_scores(symbol)
    
    proxy['average_grade'] = average_grade
    proxy['value_grade'] = value_grade
    proxy['growth_grade'] = growth_grade
    proxy['momentum_grade'] = momentum_grade
    
    proxy['pe'] = pe
    proxy['earning_yield'] = earning_yield
    proxy['pe_growth_ratio'] = pe_growth_ratio
    proxy['psales'] = psales
    proxy['pbook'] = pbook
    proxy['pcashflow'] = pcashflow
    proxy['cash_pc'] = cash_pc
    
    proxy['profit_margin'] = profit_margin

    proxy['chg_1d'] = chg_1d
    proxy['chg_5d'] = chg_5d
    proxy['chg_1m'] = chg_1m
    proxy['chg_3m'] = chg_3m
    proxy['chg_1y'] = chg_1y
    return proxy


def test1() -> None:
    #symbol: str = input('What SYMBOL do you want to check? ')
    x = get_zacks_scores('NVDA')
    print(x)


def test2() -> None:
    symbol: str = input('What SYMBOL do you want to check? ')
    proxy = proxy_zacks_scores(symbol)
    print(proxy)


if __name__ == '__main__':
    test2()
