
import sys; sys.path.append('..')

from psycopg2._psycopg import cursor




from datetime import date, datetime

from dimsumpy.database.postgres import upsertquery, upsert_dict
from batterypy.string.read import readf, readi
from batterypy.time.cal import get_trading_day, get_trading_day_utc

from multiprocessing.managers import DictProxy, SyncManager
from multiprocessing import Manager, Process

import pandas
from pandas.core.frame import DataFrame
from pandas.core.series import Series

import requests
from requests.models import Response
from requests.structures import CaseInsensitiveDict

from shared_model.st_data_model import stock_list_dict
from shared_model.sql_model import cnx, db_dict  # the postgres server must running
from timeit import default_timer

from typing import Any, List, Optional, Tuple, Union


def zacks_upsert_1s(symbol: str) -> str:
    """ test USO, QQQ, AABA, ADRO, AGEN """
    code: str = symbol.upper()
    manager: SyncManager = Manager()
    d: DictProxy = manager.dict()
    d['symbol']: str = code
    d['td']: date = get_trading_day_utc()
    d['t']: datetime = datetime.now().replace(microsecond=0)
    try:
        p1: Process = Process(target=zacks_estimates, args=(code, d))
        p2: Process = Process(target=zacks_scores, args=(code, d))
        p1.start()
        p2.start()
        p1.join()
        p2.join()


        if 'cash_per_share' in d and 'pb' in d:
            upsert_dict(table='usstock_z', dict=d, primarykeys=db_dict['usstock_z'].get('pk'), con=cnx)
            print('upserted: ', d)
        else:
            print('no upsert: ', d)

        return code
    except Exception as e:
        print(code, e)
        return (f'{code} salesupdate1s Exception: {e}')
    finally:  # To make sure processes are closed in the end, even if errors happen
        p1.close()
        p2.close()


def zacks_estimates(s: str, d: DictProxy={}) -> Optional[float]:
    try:
        headers: CaseInsensitiveDict = requests.utils.default_headers()
        headers['User-Agent']: str = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        estimates_url: str = "https://www.zacks.com/stocks/quote/" + s + "/detailed-estimates"
        estimates_r: Response = requests.get(estimates_url, headers=headers)
        estimates_dfs: List[DataFrame] = pandas.read_html(estimates_r.text, header=None)
        low_frames: bool = len(estimates_dfs) < 13

        edate_str: str = '' if low_frames else estimates_dfs[2].iloc[0, 1]
        edate_invalid: bool = (not isinstance(edate_str, str)) or '/' not in edate_str  # 'USO' type is float
        edate: Optional[date] = None if edate_invalid else datetime.strptime(edate_str.replace('*AMC','').replace('*BMO',''), '%m/%d/%y').date()
        if edate is not None:
            d['edate'] = edate

        recom_str: str = '' if low_frames else estimates_dfs[2].iloc[-1, -1]
        recom: Optional[float] = readf(recom_str)
        if recom is not None:
            d['recom'] = recom

        eps_str: str = '' if low_frames else estimates_dfs[3].iloc[1, -1]
        eps: Optional[float] = readf(eps_str)
        if eps is not None:
            d['eps'] = eps

        feps_str: str = '' if low_frames else estimates_dfs[3].iloc[2,-1]
        feps: Optional[float] = readf(feps_str)
        if feps is not None:
            d['feps'] = feps

        eps12_str: str = '' if low_frames else estimates_dfs[3].iloc[3,-1]
        eps12: Optional[float] = readf(eps12_str)
        if eps12 is not None:
            d['eps12'] = eps12

        rank_str: str = '' if low_frames else estimates_dfs[5].iloc[0,1]
        rank_invalid: bool = (not isinstance(rank_str, str)) or ' ' not in rank_str
        rankno_str: str = '' if rank_invalid else rank_str.split()[-1]
        rankno: Optional[int] = readi(rankno_str)
        rankstr: Optional[str] = None if rankno is None else rank_str[:-2]
        if rankno is not None and rankstr is not None:
            d['rankno'] = rankno
            d['rankstr'] = rankstr

        salesgrow_str: str = '' if low_frames else estimates_dfs[8].iloc[-1, -1]
        salesgrow: Optional[float] = readf(salesgrow_str[:-1])
        if salesgrow is not None:
            d['salesgrow'] = salesgrow

        egrow_str: str = '' if low_frames else estimates_dfs[9].iloc[-1, -1]
        egrow: Optional[float] = readf(egrow_str[:-1])
        if egrow is not None:
            d['egrow'] = egrow

        surprise_str: str = '' if low_frames else estimates_dfs[13].iloc[-1,-1]
        surprise: Optional[float] = readf(surprise_str[:-1])
        if surprise is not None:
            d['surprise'] = surprise

        return s
    except requests.exceptions.RequestException as e:
        print(s, 'zacks_estimates RequestException: ', e)
        return None
    except Exception as e2:
        print(s, 'zacks_estimates Exception e2: ', e2)
        return None


# scores_r.status_code will still be 200 for invalid symbols
def zacks_scores(s: str, d: DictProxy={}) -> Optional[float]:
    try:
        headers: CaseInsensitiveDict = requests.utils.default_headers()
        headers['User-Agent']: str = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        scores_url: str = "https://www.zacks.com/stock/research/" + s + "/stock-style-scores"
        scores_r: Response = requests.get(scores_url, headers=headers)

        scores_dfs: List[DataFrame] = pandas.read_html(scores_r.text, header=None)
        low_frames: bool = len(scores_dfs) < 18

        # Value Growth Momentum, grading A B C D F
        vgm_str: str = '' if low_frames else scores_dfs[9].iloc[1, 1]
        vgm_invalid: bool = (not isinstance(vgm_str, str)) or len(vgm_str) != 1
        vgm: Optional[str] = None if vgm_invalid else vgm_str
        if vgm is not None:  # vgm might be NA
            d['vgm'] = vgm

        cashyield_str: str = '' if low_frames else scores_dfs[9].iloc[2, 1]
        cashyield: Optional[float] = readf(cashyield_str)
        if cashyield is not None:
             d['cashyield'] = cashyield

        peg_str: str = '' if low_frames else scores_dfs[9].iloc[4, 1]
        peg: Optional[float] = readf(peg_str)
        if peg is not None:
            d['peg'] = peg

        pb_str: str = '' if low_frames else scores_dfs[9].iloc[5, 1]
        pb: Optional[float] = readf(pb_str)
        if pb is not None:
            d['pb'] = pb

        pcf_str: str = '' if low_frames else scores_dfs[9].iloc[6, 1]
        pcf: Optional[float] = readf(pcf_str)
        if pcf is not None:
            d['pcf'] = pcf

        pe_str: str = '' if low_frames else scores_dfs[9].iloc[7, 1]
        pe: Optional[float] = readf(pe_str)
        if pe is not None:
            d['pe'] = pe

        psales_str: str = '' if low_frames else scores_dfs[9].iloc[8, 1]
        psales: Optional[float] = readf(psales_str)
        if psales is not None:
            d['psales'] = psales

        earnyield_str: str = '' if low_frames else scores_dfs[9].iloc[9, 1]
        earnyield: Optional[float] = readf(earnyield_str[:-1])
        if earnyield is not None:
            d['earnyield'] = earnyield

        cashps_str: str = '' if low_frames else scores_dfs[9].iloc[11, 1]
        cashps: Optional[float] = readf(cashps_str)
        if cashps is not None:
            d['cash_per_share'] = cashps


        chg1d_str: str = '' if low_frames else scores_dfs[11].iloc[2, 1]
        chg1d: Optional[float] = readf(chg1d_str[:-1])
        if chg1d is not None:
            d['chg1d'] = chg1d

        chg5d_str: str = '' if low_frames else scores_dfs[11].iloc[3, 1]
        chg5d: Optional[float] = readf(chg5d_str[:-1])
        if chg5d is not None:
            d['chg5d'] = chg5d

        chg1m_str: str = '' if low_frames else scores_dfs[11].iloc[4, 1]
        chg1m: Optional[float] = readf(chg1m_str[:-1])
        if chg1m is not None:
            d['chg1m'] = chg1m

        chg3m_str: str = '' if low_frames else scores_dfs[11].iloc[5, 1]
        chg3m: Optional[float] = readf(chg3m_str[:-1])
        if chg3m is not None:
            d['chg3m'] = chg3m

        chg1y_str: str = '' if low_frames else scores_dfs[11].iloc[6, 1]
        chg1y: Optional[float] = readf(chg1y_str[:-1])
        if chg1y is not None:
            d['chg1y'] = chg1y

        return s
    except requests.exceptions.RequestException as e:
        print('zacks_scores RequestException: ', e)
        return None
    except Exception as e2:
        print('zacks_scores Exception e2: ', e2)
        return None





### TESTING LAB ###


# scores_r.status_code will still be 200 for invalid symbols
def zacks_sco(s: str, d: DictProxy={}) -> Optional[float]:
    try:
        headers: CaseInsensitiveDict = requests.utils.default_headers()
        headers['User-Agent']: str = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        # scores_url: str = "https://www.zacks.com/stock/research/" + s + "/stock-style-scores"
        # scores_r: Response = requests.get(scores_url, headers=headers)
        #
        # scores_dfs: List[DataFrame] = pandas.read_html(scores_r.text, header=None)
        # low_frames: bool = len(scores_dfs) < 18

        # Value Growth Momentum, grading A B C D F
        # vgm_str: str = '' if low_frames else scores_dfs[9].iloc[1, 1]
        # vgm_invalid: bool = (not isinstance(vgm_str, str)) or len(vgm_str) != 1
        # vgm: Optional[str] = None if vgm_invalid else vgm_str
        # if vgm is not None:  # vgm might be NA
        #     d['vgm'] = vgm
        #
        # cashyield_str: str = '' if low_frames else scores_dfs[9].iloc[2, 1]
        # cashyield: Optional[float] = readf(cashyield_str)
        # if cashyield is not None:
        #      d['cashyield'] = cashyield
        #
        # peg_str: str = '' if low_frames else scores_dfs[9].iloc[4, 1]
        # peg: Optional[float] = readf(peg_str)
        # if peg is not None:
        #     d['peg'] = peg

        return s
    except requests.exceptions.RequestException as e:
        print('zacks_scores RequestException: ', e)
        return None
    except Exception as e2:
        print('zacks_scores Exception e2: ', e2)
        return None







if __name__ == '__main__':
    stock = input('which stock do you want to check? ')

    zacks_sco(stock)
    print(default_timer())

