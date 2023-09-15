
# STANDARD LIBS
import sys; sys.path.append('..')
from datetime import date, datetime, timezone
from typing import Any, Dict, List, Tuple, Optional


# THIRD PARTY LIBS


# CUSTOM LIBS
from dimsumpy.web.crawler import get_csv_dataframe

# PROGRAM MODULES


def make_price_url(date1: date, date2: date, symbol: str) -> str:
    """
    * INDEPENDENT *
    USED BY: get_price_dataframe()
    
    must use https
    """
    datetime1 = datetime(date1.year, date1.month, date1.day)
    datetime2 = datetime(date2.year, date2.month, date2.day)
    unix_from = str(int(datetime1.replace(tzinfo=timezone.utc).timestamp()))
    unix_to = str(int(datetime2.replace(tzinfo=timezone.utc).timestamp()))
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={unix_from}&period2={unix_to}&interval=1d&events=history&crumb=OVcrHyGzap6'
    return url



def get_price_dataframe(date1, date2, symbol):
    """
    DEPENDS ON: make_price_url()
    IMPORTS: get_csv_dataframe()

    easier to debug for having 3 functions
    might have error during HK weekday night
    """
    url = make_price_url(date1, date2, symbol)
    df = get_csv_dataframe(url, header=0)
    df.columns = ['td', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
    df['symbol'] = symbol
    now = datetime.now().replace(second=0, microsecond=0)
    df['t'] = now  # program crashes if i put the now() statement here
    return df




def test():
    d1 = date(2019, 1, 1)
    d2 = date(2023, 2, 1)
    symbol = 'AMD'
    df = get_price_dataframe(d1, d2, symbol)
    print(df)

if __name__ == '__main__':
    test()