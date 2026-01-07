"""

How to determine a WEAK stock by technical figures here?
    First, I should use steepness to sort stocks, the steepness less than 1.0 is considered week. while 0.95 or 0.96 is very weak.
    Second, I can simply use RSI to read their recent price action, choose some higher numbers. if the RSI is higher recently, that means they have rebounded.


When I prepare an OrderedDict data source, I should use TODAY, not last trading day as 'TO' date, so that last trading day is included, since 'TO' date's value is not included in yahoo price source.



"""
# STANDARD LIBS

from collections import OrderedDict
from datetime import date, datetime
from functools import partial

from multiprocessing import Pool
import os
from timeit import default_timer
from typing import Any, Dict, List, Tuple, Optional



# THIRD PARTY LIBS


# CUSTOM LIBS
from batterypy.time.cal import add_trading_days, is_weekly_close
from batterypy.number.format import round0, round1, round2, round4
from dimsumpy.finance.technical import quantile, convert_to_changes, calculate_rsi, sma, steep


# PROGRAM MODULES
from pizzapy.stock_price_update.raw_price_model import get_price_odict




def calculate_historical_prices(odict: OrderedDict[date, float], td: date) -> Any:
    """
    * INDEPENDENT *
    IMPORTS: add_trading_days()
    USED BY: get_target_prices()
    """
    td_price = odict.get(td)
    p20 = odict.get(add_trading_days(td, -20))
    p50 = odict.get(add_trading_days(td, -50))
    p100 = odict.get(add_trading_days(td, -100))
    p250 = odict.get(add_trading_days(td, -250))
    p500 = odict.get(add_trading_days(td, -500))
    if p20 is None:
        p20 = odict.get(add_trading_days(td, -21))
    if p50 is None:
        p50 = odict.get(add_trading_days(td, -51))
    return td_price, p20, p50, p100, p250, p500




def calculate_changes(prices: List[float], p20: Optional[float], p50: Optional[float]) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float]]:
    """
    * INDEPENDENT *
    IMPORTS: convert_to_changes(), quantile()
    USED BY: get_target_prices()
    """

    list_of_20_day_changes = convert_to_changes(20, prices) if prices else []
    list_of_50_day_changes = convert_to_changes(50, prices) if prices else []

    increase20 = quantile(0.98, list_of_20_day_changes) if list_of_20_day_changes else None
    decrease20 = quantile(0.02, list_of_20_day_changes) if list_of_20_day_changes else None
    increase50 = quantile(0.98, list_of_50_day_changes) if list_of_50_day_changes else None
    decrease50 = quantile(0.02, list_of_50_day_changes) if list_of_50_day_changes else None
    
    best20 = p20 * (1.0 + increase20) if p20 and increase20 else None
    worst20 = p20 * (1.0 + decrease20) if p20 and decrease20 else None
    best50 = p50 * (1.0 + increase50) if p50 and increase50 else None
    worst50 = p50 * (1.0 + decrease50) if p50 and decrease50 else None
    return increase20, decrease20, increase50, decrease50, best20, worst20, best50, worst50




def get_target_prices(td_odict: OrderedDict[date, float], td: date) -> Any:

    """
    DEPENDS ON:  calculate_historical_prices(), calculate_changes()

    USED BY: compute_technical_values()

    td_odict's length is 501 if all data available, that is 2 years data before td

    td_odict argument needs to be descending in dates, that is latest dates are placed at the front.
    """
    td_price, p20, p50, p100, p200, p500 = calculate_historical_prices(td_odict, td)

    odict_is_valid: bool = len(td_odict) > 497 and td in td_odict

    prices = list(td_odict.values()) if odict_is_valid else []
    
    increase20, decrease20, increase50, decrease50, best20, worst20, best50, worst50 = calculate_changes(prices, p20, p50)
    
    gain20 = (best20 - td_price) / td_price if td_price and best20 else None
    fall20 = (td_price - worst20) / td_price if td_price and worst20 else None
    gain50 = (best50 - td_price) / td_price if td_price and best50 else None
    fall50 = (td_price - worst50) / td_price if td_price and worst50 else None

    return td_price, p20, p50, p100, p200, p500, increase20, decrease20, increase50, decrease50, best20, worst20, best50, worst50, gain20, fall20, gain50, fall50



def get_moving_averages(td_prices: List[float]) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float]]:
    """
    IMPORTS: sma(), steep()
    USED BY: compute_technical_values()
    """
    td_price: Optional[float] = td_prices[0] if td_prices else None
    ma20: Optional[float] = sma(20, td_prices)
    ma50: Optional[float] = sma(50, td_prices)
    ma250: Optional[float] = sma(250, td_prices)
    steep20: Optional[float]  = steep(20, td_prices)
    steep50: Optional[float]  = steep(50, td_prices)
    steep250: Optional[float]  = steep(250, td_prices)
    ma50_distance = (td_price - ma50) / ma50 if td_price and ma50 else None
    ma250_distance = (td_price - ma250) / ma250 if td_price and ma250 else None
    return ma20, ma50, ma250, steep20, steep50, steep250, ma50_distance, ma250_distance




def get_weekly_rsi(odict: OrderedDict[date, float], td: date) -> Optional[float]:
    """
    * INDEPENDENT *
    IMPORTS: is_weekly_close(), calculate_rsi()
    USED BY: get_technical_values()

    typical RSI input list needs to be at least 14 * 14 + 1 days, that is 197 trading days.
    Weekly RSI requires 197 * 5, approximately 1000 trading days
    
    """

    d1000 = add_trading_days(td, -999)
    four_year_odict = OrderedDict((key, value) for key, value in odict.items() if d1000 <= key <= td)
    first_item = four_year_odict.popitem(last=False) # remove the first item from four_year_odict
        
    weekly_prices: List[float] = [first_item[1]] + [value for key, value in four_year_odict.items() if is_weekly_close(key)]
    weekly_rsi = calculate_rsi(14, weekly_prices) if first_item[0] == td else None

    return weekly_rsi    



def check_top_bottom(odict: OrderedDict[date, float], td: date) -> Tuple[Optional[int],Optional[int]]:
    """
    * INDEPENDENT *
    IMPORTS: add_trading_days()
    USED BY: get_technical_values()

    the length is sometime 49.
    """
    td_price = odict.get(td)

    plus_50_prices = [value for (key, value) in odict.items() if td < key < add_trading_days(td, 51)]

    length: int = len(plus_50_prices)
    is_top: Optional[int] = int(all(td_price > p for p in plus_50_prices)) if length > 48 and td_price else None
    
    is_bottom: Optional[int] = int(all(td_price < p for p in plus_50_prices)) if length > 48 and td_price else None
    return is_top, is_bottom



def get_td_odict_500(odict: OrderedDict[date, float], td: date) -> OrderedDict[date, float]:
    """
    * INDEPENDENT *
    IMPORTS: add_trading_days()
    USED BY: get_technical_values()

    """
    d500 = add_trading_days(td, -500)
    td_odict = OrderedDict((key, value) for key, value in odict.items() if d500 <= key <= td)
    return td_odict



def compute_technical_values(odict: OrderedDict[date, float], td: date) -> Any:
    """
    DEPENDS ON: get_moving_averages(), get_weekly_rsi(), check_top_bottom(), get_td_odict_500(), get_target_prices()
    IMPORTS: calculate_rsi(), round1(), round2(), round4()
    USED BY: 
    
    steep20 requires minimum length of list_x = 20 * 3 + 5 = 65
    steep50 requires minimum length of list_x = 50 * 3 + 5 = 155
    steep250 requires minimum length of list_x = 250 * 3 + 5 = 755
    steep() input list can be very long list, the function will cut the required length by itself
    """
    td_prices: List[float] = [value for key, value in odict.items() if key <= td] if td in odict else []
    
    ma20, ma50, ma250, steep20, steep50, steep250, ma50_distance, ma250_distance = get_moving_averages(td_prices)
    
    rsi: Optional[float] = calculate_rsi(14, td_prices)
    
    weekly_rsi: Optional[float] = get_weekly_rsi(odict, td)

    is_top, is_bottom = check_top_bottom(odict, td)

    td_odict_500 = get_td_odict_500(odict, td)
    
    td_price, p20, p50, p100, p200, p500, increase20, decrease20, increase50, decrease50, best20, worst20, best50, worst50, gain20, fall20, gain50, fall50 = get_target_prices(td_odict_500, td)
    
    technical_values = round2(ma20), round2(ma50), round2(ma250), round4(steep20), \
        round4(steep50), round4(steep250), round4(ma50_distance), round4(ma250_distance), \
        round2(rsi), round2(weekly_rsi), is_top, is_bottom, \
        round2(td_price), round2(p20), round2(p50), round2(p100), round2(p200), round2(p500), \
        round2(increase20), round2(decrease20), round2(increase50), round2(decrease50), \
        round1(best20), round1(worst20), round1(best50), round1(worst50), \
        round4(gain20), round4(fall20), round4(gain50), round4(fall50)
    
    return technical_values



def make_technical_proxy(odict: OrderedDict[date, float], SYMBOL: str, td: date) -> Dict:
    """
    DEPENDS ON: compute_technical_values()
    IMPORTS: datetime
    USED BY: 

    pairs argument is a dataset of extended dates, it is FROM-1000 till TO+50
    """
    
    ma20, ma50, ma250, steep20, \
        steep50, steep250, ma50_distance, ma250_distance, \
        rsi, weekly_rsi, is_top, is_bottom, \
        td_price, p20, p50, p100, p200, p500, \
        increase20, decrease20, increase50, decrease50, \
        best20, worst20, best50, worst50, \
        gain20, fall20, gain50, fall50 = compute_technical_values(odict, td)
        
    proxy: Dict = {}
    proxy['symbol'] = SYMBOL
    proxy['td'] = td
    proxy['t'] = datetime.now().replace(second=0, microsecond=0)
    
    proxy['ma20'] = ma20
    proxy['ma50'] = ma50 
    proxy['ma250'] = ma250 
    proxy['steep20'] = steep20

    proxy['steep50'] = steep50 
    proxy['steep250'] = steep250 
    proxy['ma50_distance'] = ma50_distance 
    proxy['ma250_distance'] = ma250_distance 

    proxy['rsi'] = rsi
    proxy['weekly_rsi'] = weekly_rsi    
    proxy['is_top'] = is_top
    proxy['is_bottom'] = is_bottom
    
    proxy['price'] = td_price
    proxy['p20'] = p20
    proxy['p50'] = p50
    proxy['p100'] = p100
    proxy['p200'] = p200
    proxy['p500'] = p500
    
    proxy['increase20'] = increase20
    proxy['decrease20'] = decrease20
    proxy['increase50'] = increase50
    proxy['decrease50'] = decrease50

    proxy['best20'] = best20
    proxy['worst20'] = worst20
    proxy['best50'] = best50
    proxy['worst50'] = worst50

    proxy['gain20'] = gain20
    proxy['fall20'] = fall20
    proxy['gain50'] = gain50
    proxy['fall50'] = fall50

    return proxy




def make_odict(FROM: date, TO: date, SYMBOL: str) -> OrderedDict[date, float]:
    """
    IMPORTS: get_price_odict()
    USED BY: 

    """
    earlier_from = add_trading_days(FROM, -1000)
    later_to = add_trading_days(TO, 51)
    odict: OrderedDict[date, float] = get_price_odict(earlier_from, later_to, SYMBOL, ascending=False)
    return odict



def construct_technical_proxies(FROM: date, TO: date, SYMBOL: str) -> List[Any]:
    """
    DEPENDS ON: make_odict(), make_technical_proxy()
    IMPORTS: os, partial()
    do not use kwargs in partial()

    td_adjclose_pairs is a dataset of extended dates, it is FROM-1000 till TO+50

    """
    odict = make_odict(FROM, TO, SYMBOL)
    
    from_to_trading_dates: List[date] = [key for (key, _) in odict.items() if FROM <= key <= TO]
    
    with Pool(os.cpu_count()) as pool:
        proxies: List[Any] = pool.map(partial(make_technical_proxy, odict, SYMBOL), from_to_trading_dates) 
    return proxies



def test():
    FROM = date(2023, 9, 19)
    TO = date(2023, 9, 22)

    xs = construct_technical_proxies(FROM, TO, 'AMD')

    for d in xs:
        print(d)
        print('\n\n')
    


if __name__ == '__main__':
    test()





