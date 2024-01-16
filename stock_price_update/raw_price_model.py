"""
AIM:
To get a price dataframe out of FROM TO date range.

USED BY: price_update_database_model.py
"""
# STANDARD LIBS

from collections import OrderedDict
from datetime import date, datetime, timezone
from typing import Any, Dict, List, Tuple, Optional


# THIRD PARTY LIBS
from pandas import DataFrame, to_datetime

# CUSTOM LIBS
from dimsumpy.web.crawler import get_csv_dataframe

# PROGRAM MODULES


def make_price_url(FROM: date, TO: date, SYMBOL: str) -> str:
    """
    * INDEPENDENT *
    USED BY: get_price_dataframe()
    
    must use https
    """
    datetime1 = datetime(FROM.year, FROM.month, FROM.day)
    datetime2 = datetime(TO.year, TO.month, TO.day)
    unix_from = str(int(datetime1.replace(tzinfo=timezone.utc).timestamp()))
    unix_to = str(int(datetime2.replace(tzinfo=timezone.utc).timestamp()))
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{SYMBOL}?period1={unix_from}&period2={unix_to}&interval=1d&events=history&crumb=OVcrHyGzap6'
    return url



def get_price_dataframe(FROM, TO, SYMBOL, ascending=True) -> DataFrame:
    """
    DEPENDS ON: make_price_url()
    IMPORTS: get_csv_dataframe()
    USED BY: get_price_odict()

    the result set DOES NOT include TO date, only the previous day of TO date.
    """
    url = make_price_url(FROM, TO, SYMBOL)
    df = get_csv_dataframe(url, header=0)
    df.columns = ['td', 'open', 'high', 'low', 'close', 'adjclose', 'volume']

    #df['td'] = datetime.strptime(df['td'], '%Y-%m-%d')
    df['symbol'] = SYMBOL 
    
    now = datetime.now().replace(second=0, microsecond=0)
    df['t'] = now  # program crashes if i put the datetime.now() statement on this line directly after the equal sign.
    return df.sort_values(by='td', ascending=ascending)



def get_price_odict(FROM, TO, SYMBOL, ascending=True) -> OrderedDict[date, float]:
    """
    DEPENDS ON: get_price_dataframe()
    IMPORTS: datetime, OrderedDict

    the result set DOES NOT include TO date, only the previous day of TO date.
    """
    price_df: DataFrame = get_price_dataframe(FROM, TO, SYMBOL, ascending=ascending)
    string_price_odict: OrderedDict[str, float] = price_df.set_index('td')['adjclose'].to_dict(into=OrderedDict)

    date_price_odict: OrderedDict[date, float] = OrderedDict((datetime.strptime(key, '%Y-%m-%d').date(), value) for key, value in string_price_odict.items()) 
    return date_price_odict




def get_price_dataframe_odict(FROM, TO, SYMBOL, ascending=True) -> Tuple[DataFrame, OrderedDict[date, float]]:
    """
    DEPENDS ON: get_price_dataframe()
    IMPORTS: datetime, OrderedDict

    the result set DOES NOT include TO date, only the previous day of TO date.
    """
    price_df: DataFrame = get_price_dataframe(FROM, TO, SYMBOL, ascending=ascending)
    string_price_odict: OrderedDict[str, float] = price_df.set_index('td')['adjclose'].to_dict(into=OrderedDict)

    date_price_odict: OrderedDict[date, float] = OrderedDict((datetime.strptime(key, '%Y-%m-%d').date(), value) for key, value in string_price_odict.items()) 
    return price_df, date_price_odict




def test():
    d1 = date(2023, 4, 3)
    d2 = date(2023, 4, 4)
    symbol = 'NVDA'
    x = get_price_dataframe(d1, d2, symbol)
    print(x)
    

if __name__ == '__main__':
    test()