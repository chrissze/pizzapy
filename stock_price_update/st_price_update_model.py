import os
import sys;
from functools import partial
from multiprocessing import Pool
from timeit import default_timer

from dimsumpy.finance.technical import ema, quantile, deltas, changes, rsi_calc, steep

sys.path.append('..')

from batterypy.fp.list import first, grab

from itertools import dropwhile, repeat
from multiprocessing.managers import DictProxy
from typing import Any, Dict, List, Tuple, Optional
from batterypy.time.cal import add_trading_days, date_range, tdate_range, tdate_length, date_length, \
    get_trading_day_utc, is_weekly_close

from psycopg2 import connect


from psycopg2.extensions import connection, cursor



from datetime import date, datetime, timezone
import io


import requests
import pandas as pd

from shared_model.sql_model import pg_db, pg_user, pg_pass, pg_host, cnx, db_dict  # the postgres server must running, error if not
from dimsumpy.database.postgres import upsertquery, upsert_dict


# must use https
def ya_construct_url(date1: date, date2: date, symbol: str) -> str:
    dt1 = datetime(date1.year, date1.month, date1.day)
    dt2 = datetime(date2.year, date2.month, date2.day)
    unix_from = str(int(dt1.replace(tzinfo=timezone.utc).timestamp()))
    unix_to = str(int(dt2.replace(tzinfo=timezone.utc).timestamp()))
    url = "".join(["https://query1.finance.yahoo.com/v7/finance/download/"
                   , symbol, "?period1=", unix_from, "&period2=", unix_to
                   , "&interval=1d&events=history&crumb=OVcrHyGzap6"])
    return url


# easier to debug for having 3 functions
# might have error during HK weekday night
def ya_parse_csv(date1, date2, symbol):
    try:
        url = ya_construct_url(date1, date2, symbol)
        #r = requests.post(url)
        r = requests.get(url)
        now = datetime.now().replace(microsecond=0)
        #print(r.text)
        df = pd.read_csv(io.StringIO(r.text), header=0)
        df.columns = ['td', 'op', 'hi', 'lo', 'cl', 'adjcl', 'vol']
        df['symbol'] = symbol
        df['t'] = now  # program crashes if i put the now() statement here
        return df
    except requests.exceptions.RequestException as e:
        print('Request Exception: ', str(e))
        return pd.DataFrame()
    except Exception as e2:
        print(url)
        print('yacsv,', str(e2))
        return pd.DataFrame()

# from is a reserved word, to is not
def ya_px_upsert_1s(from_: date, to: date, symbol: str) -> str:
    """
    d1 = date(2017, 2, 25)
    d2 = date(2017, 5, 10)
    xx = ya_px_upsert_1s(d1, d2, 'AAPL')
    print(xx)
    """
    code = symbol.upper()
    # I make a custum connection here to prevent postgres stuck on invalid sql commands.
    # I can re-open/close this custom connection
    cnx: connection = connect(dbname=pg_db, user=pg_user, password=pg_pass, host=pg_host)
    c: cursor = cnx.cursor()
    try:
        df = ya_parse_csv(from_, to, code)
        print('finished downloading dataframe ')
        entries = [] if df.empty else [tuple(r) for r in df.values]
        q = upsertquery('usstock_price', df.columns, ['symbol', 'td'])
        print('len_entries:', len(entries))

        if entries: # delete not soon
            c.executemany(q, entries)
            c.close()
            cnx.commit()
            result_str = ' '.join([symbol, str(from_), str(to), str(len(entries)), 'rows upserted,'
                         , str(c.rowcount), 'in which newly inserted'])
            return result_str
        else:
            return 'ya_px_upsert_1s empty entry'
    except Exception as e:
        if cnx:
            c.close()
            cnx.close()
        return 'ya_px_upsert_1s Exception e: ' + str(e)

def verify():

    d1 = date(2000, 1, 1)
    d2 = date(2020, 5, 31)
    dd = tdate_length(d1, d2)
    print(dd)
    pairs = get_st_price_pairs(d1, d2, 'MSFT', cnx)
    tds = sorted([x[0] for x in pairs])
    theory_tds = tdate_range(d1, d2)

    print('len_tds :', len(tds))
    print('len_theo:', len(theory_tds))

    print('tds :', tds)
    print('theo:', theory_tds)


def tech_upsert_1s(from_: date, to: date, code: str) -> str:
    past_day = add_trading_days(from_, -1000)
    later_day = add_trading_days(to, 20)

    extended_pairs: List[Any] = get_st_price_pairs(past_day, later_day, code, cnx)
    ext_len = len(extended_pairs)
    from_to_dates: List[date] = [x[0] for x in extended_pairs if from_ <= x[0] <= to]

    ltd = get_trading_day_utc()
    theory_len = tdate_length(past_day, min(ltd, later_day))
    #print('ext_len', ext_len)
    #print('theory len:', theory_len)


    valid = (theory_len - ext_len) < 3
    if valid:
        with Pool(os.cpu_count()) as pool:
            pool.map(partial(st_chg_calc, code, extended_pairs), from_to_dates) # do not use kwargs


    else:
        print('theory_len:', theory_len)
        print('ext_len:', ext_len)
        print('valid: ', valid)
        return (f' - no tech_upsert')
    return 'done'


def get_st_price_pairs(from_: date, to: date, symbol: str, con: connection) -> List[Any]:
    try:
        sql = f"""SELECT td, adjcl FROM usstock_price WHERE symbol = '{symbol}' AND 
        td >= '{from_.isoformat()}' AND td <= '{to.isoformat()}' ORDER BY td DESC"""
        df: pd.DataFrame = pd.read_sql(sql, con=con)  # compatible to different db, no error for empty result
        pairs: List[Any] = [tuple(x) for x in df.values]
        #print(pairs)
        return pairs
    except Exception as e:
        print(f"get_st_prices: {e}")
        return []


def st_chg_calc(symbol:str, pairs: List[Tuple[date, float]], td: date) -> None:
    # I must place td at last because it is the iterable argument
    # if i create a connection here, it will be expensive
    d = {}
    d['t']: datetime = datetime.now().replace(microsecond=0)
    d['symbol'] = symbol
    d['td'] = td
    tuples = list(dropwhile(lambda x: x[0] > td, pairs))
    prices: List[float] = [px for (_, px) in tuples]
    weekly_prices = prices[:1] + [x[1] for x in tuples[1:] if is_weekly_close(x[0])]
    fut_past_prices = [x[1] for x in pairs if add_trading_days(td, -21) < x[0] < add_trading_days(td, 21) and x[0] != td]

    #print('fut_past_prices, ', fut_past_prices)
    #print('Fut_past length: ', len(fut_past_prices))

    d['px'] = (px := first(prices))
    d['p20'] = (p20 := grab(prices, 20))
    d['p50'] = (p50 := grab(prices, 50))
    d['p125'] = grab(prices, 125)
    d['p200'] = grab(prices, 200)
    list20 = changes(20, prices[:421])
    list50 = changes(50, prices[:451])
    ch2002 = quantile(0.02, list20)
    ch2098 = quantile(0.98, list20)
    ch5002 = quantile(0.02, list50)
    ch5098 = quantile(0.98, list50)
    tg2002 = p20 * (1.0 + ch2002)
    tg2098 = p20 * (1.0 + ch2098)
    tg5002 = p50 * (1.0 + ch5002)
    tg5098 = p50 * (1.0 + ch5098)


    rsi = rsi_calc(14, prices)
    wrsi = rsi_calc(14, weekly_prices)
    ema20 = ema(20, prices)
    ema50 = ema(50, prices)
    steep20 = steep(20, prices)
    steep50 = steep(50, prices)

    istop: Optional[bool] = None if len(fut_past_prices) != 40 else all(x < px for x in fut_past_prices)
    isbot: Optional[bool] = None if len(fut_past_prices) != 40 else all(x > px for x in fut_past_prices)
    # print(tg2002)
    # print(tg2098)
    # print(tg5002)
    # print(tg5098)
    # print(rsi)
    # print(wrsi)
    # print(ema20)
    # print(ema50)
    # print(steep20)
    # print(steep50)
    if istop: print(symbol, 'istop', istop, px, td, steep20)
    if isbot: print(symbol, 'isbot', isbot, px, td, tg2002, tg5002, rsi,wrsi, steep20)

    #print(d)
    #upsert_dict(table='usstock_tech', dict=d, primarykeys=db_dict['usstock_tech'].get('pk'), con=cnx)


def calc_up(lst) -> bool:
    em20 = ema(lst, 20)
    em125 = ema(lst, 125)
    return em20 > em125


def mytest():
    d1 = date(2018, 1, 1)
    d2 = date(2020, 4, 30)
    #ya_px_upsert_1s(d1, d2,'C')
    xx = tech_upsert_1s(from_=d1, to=d2, code='MSFT')
    #xx = get_st_price_pairs(d1, d2, 'C', cnx)

    print(default_timer())

if __name__ == '__main__':
    mytest()