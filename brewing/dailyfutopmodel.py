import sys
sys.path.append('..')



import io
from typing import List, Tuple
from multiprocessing import Manager, Pool

import requests
import pandas as pd
from bs4 import BeautifulSoup

from shared_model.fut_data_model import fut_dict


manager = Manager()
callmoneylist = manager.list([])
putmoneylist = manager.list([])

def processurl(url: str):
    cm, pm = inotable(url)
    callmoneylist.append(cm)
    putmoneylist.append(pm)

def inooption(code: str) -> Tuple[float, float]:
    urls = inomonths(code)
    print(urls)

    with Pool(processes=6) as pool:
        callmoneylist[:] = []
        putmoneylist[:] = []
        pool.map(processurl, urls)

    lot = fut_dict[code]['lot']
    callmoney = float(sum(callmoneylist)) * lot
    putmoney = float(sum(putmoneylist)) * lot
    totalmoney = callmoney + putmoney
    callpct = callmoney / totalmoney * 100
    putpct = putmoney / totalmoney * 100
    return callpct, putpct


def inotable(url: str) -> Tuple[float, float]:
    try:
        r = requests.get(url)
        dfs = pd.read_html(r.text, header=1)
        df = dfs[1]
        #print(df.shape)
        is_valid = df.shape[1] == 10 and df.shape[0] > 0 and df.dtypes[3] == df.dtypes[5] == df.dtypes[7] == df.dtypes[9]
        if is_valid:
            df.columns = ['expiration', 'strike', 'csym', 'clast', 'cchange', 'coi', 'psym', 'plast', 'pchange', 'poi']
            df.fillna(0, inplace=True)
            df['cm'] = df.clast * df.coi
            df['pm'] = df.plast * df.poi
            return df.cm.sum(), df.pm.sum()
        else:
            return 0.0, 0.0
    except Exception as e:
        print('inotable', str(e))


def inomonths(code: str) -> List[str]:
    try:
        def createurl(s): return ''.join(['http://quotes.ino.com/options/?s=', exchange, '_', s])
        month_drop = fut_dict[code]['monthdrop']
        exchange = fut_dict[code]['exchange']
        url = ''.join(['http://quotes.ino.com/exchanges/contracts.html?r=', exchange, '_', code])
        #print(url)
        r = requests.get(url)
        #print(r.text)
        df = pd.read_html(r.text, header=2)
        df_col0 = df[0].iloc[0:, 0]
        ino_months = list(filter(lambda s: len(s) < 7, df_col0))
        op_urls = list(map(createurl, ino_months[month_drop:]))
        return op_urls
    except Exception as e:
        print('inomonths', str(e))

if __name__ == '__main__':
    #aaa = fut_dict['NG']['type']
    #cp, pp = inooption('GC')
    #print(cp, pp)
    #cmeoi('GC')