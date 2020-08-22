import sys;sys.path.append('..')

from bs4 import BeautifulSoup, ResultSet


import urllib.request as request
from batterypy.string.read import is_floatable, readf
import io
import pandas as pd
from pandas.core.frame import DataFrame
from PySide2.QtCore import (QDate, QDateTime ,
                            QModelIndex, QRegExp ,QSortFilterProxyModel, Qt)
import requests
from requests.models import Response
from typing import Any, Dict, List, Set, Union
from shared_model.stock_list import sp_500_stocks, nasdaq_100_stocks, nasdaq_traded_stocks, nasdaq_listed_stocks, \
    option_stocks, russell_2000_stocks


class MySortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs) -> None:
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.filters: Dict[Union[int, str], QRegExp] = {}

    def setFilterByColumn(self, regex: QRegExp, column: int) -> None:
        if regex.patternSyntax() == QRegExp.PatternSyntax.RegExp:
            self.filters[column]: QRegExp = regex
        else:
            self.filters[str(column)]: QRegExp = regex
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        for key, regex in self.filters.items():
            if regex.patternSyntax() == QRegExp.PatternSyntax.RegExp:
                ix: QModelIndex = self.sourceModel().index(source_row, key, source_parent)
                if ix.isValid():
                    celltext: str = self.sourceModel().data(ix)
                    regextext: str = regex.pattern()
                    result: bool = float(regextext) > float(celltext) if is_floatable(celltext) \
                        and is_floatable(regextext) else regex.indexIn(celltext)
                    if result:
                        return False
            else:
                ix: QModelIndex = self.sourceModel().index(source_row, int(key), source_parent)
                if ix.isValid():
                    celltext: str = self.sourceModel().data(ix)
                    regextext: str = regex.pattern()
                    result: bool = float(regextext) < float(celltext) if is_floatable(celltext) \
                        and is_floatable(regextext) else regex.indexIn(celltext)
                    if result:
                        return False
        return True

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        leftstr: str = left.data()
        rightstr: str = right.data()
        leftdat: Union[str, float] = leftstr if not is_floatable(leftstr) else float(leftstr)
        rightdat: Union[str, float] = rightstr if not is_floatable(rightstr) else float(rightstr)
        return leftdat < rightdat


def get_sp_500() -> List[str]:
    try:
        r: Response = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
        dfs: List[DataFrame] = pd.read_html(r.text, header=0)
        stocks: List[str] = list(dfs[0].iloc[0:, 0])
        return stocks
    except requests.exceptions.RequestException as e:
        print('getsp500 error e:', e)
        return []
    except Exception as e2:
        print('getsp500 error e2:', e2)
        return []




def get_nasdaq_100() -> List[str]:
    try:
        r: Response = requests.get("https://en.wikipedia.org/wiki/NASDAQ-100")
        soup: BeautifulSoup = BeautifulSoup(r.text, 'html.parser')
        soup_item: ResultSet = soup.find('table', id='constituents')
        dfs: List[DataFrame] = pd.read_html(str(soup_item), header=0)
        stocks: List[str] = list(dfs[0].iloc[0:, 1])
        return stocks
    except requests.exceptions.RequestException as e:
        print('get_nasdaq_100 error e:', e)
        return []
    except Exception as e2:
        print('get_nasdaq_100 error e2:', e2)
        return []




def get_nasdaq_listed() -> List[str]:
    try:
        url1 = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt'
        with request.urlopen(url1) as r:
            text = r.read().decode()
        df_nasdaq: DataFrame = pd.read_csv(io.StringIO(text), sep='|', header=0)
        stocks: List[str] = list(df_nasdaq.iloc[:-1, 0])
        return stocks
    except Exception as e:
        print('getnasdaq error:', e)
        return []


def get_nasdaq_traded() -> List[str]:
    try:
        url1 = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqtraded.txt'
        with request.urlopen(url1) as r:
            text = r.read().decode()
        df_nasdaq: DataFrame = pd.read_csv(io.StringIO(text), sep='|', header=0)
        stocks: List[str] = list(df_nasdaq.iloc[:-1, 1])
        return stocks
    except Exception as e:
        print('get_nasdaq_traded error:', e)
        return []


def get_option_traded() -> List[str]:
    """ file size is about 50mb, unique symbols are about 3129"""
    try:
        url1 = 'ftp://ftp.nasdaqtrader.com/SymbolDirectory/options.txt'
        with request.urlopen(url1) as r:
            text = r.read().decode()
        df_nasdaq: DataFrame = pd.read_csv(io.StringIO(text), sep='|', header=0)
        stocks: List[str] = list(df_nasdaq.iloc[:-1, 0])
        stocks_set = sorted(list(set(stocks)))
        return stocks_set
    except Exception as e:
        print('get_option_traded error:', e)
        return []


def get_russell_2000() -> List[str]:
    try:
        file_a = 'russell-2000-a.csv'
        file_z = 'russell-2000-z.csv'
        with open(file_a) as f1, open(file_z) as f2:
            text1 = f1.read()
            text2 = f2.read()
        df_russell_1: DataFrame = pd.read_csv(io.StringIO(text1), sep=',', header=0)
        df_russell_2: DataFrame = pd.read_csv(io.StringIO(text2), sep=',', header=0)
        stocks_a: List[str] = list(df_russell_1.iloc[0:, 0])
        stocks_z: List[str] = list(df_russell_2.iloc[0:, 0])
        stocks = sorted(stocks_a + stocks_z)
        return stocks
    except Exception as e:
        print('get_nasdaq_traded error:', e)
        return []




sp_500_nasdaq_100: List[str] = sorted(list(set(sp_500_stocks + nasdaq_100_stocks)))

all_stocks = nasdaq_traded_stocks + ['ATHM']

stock_list_dict: Dict[str, List[str]] = {
    f'S&P 500 + Nasdqa 100 ({len(sp_500_nasdaq_100)})': sp_500_nasdaq_100,
    f'S&P 500 ({len(sp_500_stocks)})': sp_500_stocks,
    f'Nasdaq 100({len(nasdaq_100_stocks)})': nasdaq_100_stocks,
    f'Option Stocks ({len(option_stocks)})': option_stocks,
    f'Nasdaq Listed({len(nasdaq_listed_stocks)})': nasdaq_listed_stocks,
    f'Nasdaq Traded({len(nasdaq_traded_stocks)})': nasdaq_traded_stocks,
    f'Russell 2000({len(russell_2000_stocks)})': russell_2000_stocks,
    f'All Stocks ({len(all_stocks)})': all_stocks,
}



def stock_list_writer() -> None:
    file_import: str = 'from typing import Any, Dict, List'
    nasdaq_100: List[str] = get_nasdaq_100()
    nasdaq_100_str: str = f'# {len(nasdaq_100)} \nnasdaq_100_stocks: List[str] = {nasdaq_100}'
    sp_500: List[str] = get_sp_500()
    sp_500_str: str = f'# {len(sp_500)} \nsp_500_stocks: List[str] = {sp_500}'
    option: List[str] = get_option_traded()
    option_str: str = f'# {len(option)} \noption_stocks: List[str] = {option}'
    nasdaq_listed: List[str] = get_nasdaq_listed()
    nasdaq_listed_str: str = f'# {len(nasdaq_listed)} \nnasdaq_listed_stocks: List[str] = {nasdaq_listed}'
    nasdaq_traded: List[str] = get_nasdaq_traded()
    nasdaq_traded_str: str = f'# {len(nasdaq_traded)} \nnasdaq_traded_stocks: List[str] = {nasdaq_traded}'
    russell_2000: List[str] = get_russell_2000()
    russell_2000_str: str = f'# {len(russell_2000)} \nrussell_2000_stocks: List[str] = {russell_2000}'

    content: str = f"""{file_import}
{nasdaq_100_str}
{sp_500_str}
{option_str}
{nasdaq_listed_str}
{nasdaq_traded_str}
{russell_2000_str}
"""
    filename = 'stock_list.py'
    with open(filename, 'w') as f:
        f.write(content)
    print(f'write {filename} done')
    return None



if __name__ == '__main__':
    stock_list_writer()

    print('done')
