# STANDARD LIBS
import sys; sys.path.append('..')

from typing import Any, List, Optional, Tuple, Union
from multiprocessing.managers import DictProxy


# THIRD PARTY LIBS

# CUSTOM LIBS
from dimsumpy.database.postgres import upsert_dict

# PROGRAM MODULES
from guru_proxy_model import proxy_guru_wealth
from shared_model.sql_model import cnx, db_dict  # the remote postgres server must running



def upsert_guru(symbol: str) -> None:
    '''
    DEPENDS: proxy_guru_wealth, upsert_dict, cnx, db_dict
    '''
    proxy: DictProxy = proxy_guru_wealth(symbol)
    valid_data: bool = proxy.get('wealth_pc') is not None

    if valid_data:
        upsert_dict(table='usstock_g', dict=proxy, primarykeys=db_dict['usstock_g'].get('pk'), con=cnx)







def try_upsert_guru(symbol: str) -> None:
    try:
        upsert_guru(symbol)
    except Exception as error:
        print('try_upsert_guru error: ', error)
    


if __name__ == '__main__':

    s = input('which string to input? ')

    x = upsert_guru(s)

    print(x)

