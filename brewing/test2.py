from datetime import date

from batterypy.time.cal import get_trading_day_utc
from batterypy.fp.list import head, last, z, grab

from shared_model.fut_data_model import fut_dict
from shared_model.sql_model import db_dict

xs = (1,2,3,4)

xx = grab(xs, 3)

print(xx)



print( [1,2,3,4] |z| 4)
