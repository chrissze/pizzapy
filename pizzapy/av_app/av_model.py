


# STANDARD LIB

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
import os
from time import sleep
from typing import Literal


# THIRD

from alpha_vantage.fundamentaldata import FundamentalData

from alpha_vantage.timeseries import TimeSeries

import requests

#CUSTOM
from batterypy.string.read import is_floatable, readf



API_KEY = os.getenv('AV_API_KEY')

@dataclass
class OptionPosition:
    contractID: str
    symbol: str
    expiration: date
    strike: Decimal
    type: Literal["call", "put"]
    last: float | None
    mark: Decimal
    bid: Decimal
    bid_size: int
    ask: Decimal
    ask_size: int
    volume: int
    open_interest: float | None
    date: date
    implied_volatility: float
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float

    @classmethod
    def from_dict(cls, data: dict) -> "OptionPosition":
        """Create an OptionContract from a raw API response dict."""
        return cls(
            contractID=data["contractID"] if data.get('contractID') is not None else None,
            symbol=data["symbol"] if data.get('symbol') is not None else None,
            expiration=date.fromisoformat(data["expiration"]) if data.get('expiration') is not None else None,
            strike=readf(data.get("strike")),
            type=data["type"] if data.get('type') is not None else None,
            last=float(data["last"]) if data.get('last') is not None else None,
            mark=Decimal(data["mark"]) if data.get('mark') is not None else None,
            bid=Decimal(data["bid"]) if data.get('bid') is not None else None,
            bid_size=int(data["bid_size"]) if data.get('bid_size') is not None else None,
            ask=Decimal(data["ask"]) if data.get('ask') is not None else None,
            ask_size=int(data["ask_size"]) if data.get('ask_size') is not None else None,
            volume=int(data["volume"]) if data.get('volume') is not None else None,
            open_interest=readf(data.get("open_interest")),
            date=date.fromisoformat(data["date"]) if data.get('date') is not None else None,
            implied_volatility=float(data["implied_volatility"]) if data.get('implied_volatility') is not None else None,
            delta=float(data["delta"]) if data.get('delta') is not None else None,
            gamma=float(data["gamma"]) if data.get('gamma') is not None else None,
            theta=float(data["theta"]) if data.get('theta') is not None else None,
            vega=float(data["vega"]) if data.get('vega') is not None else None,
            rho=float(data["rho"]) if data.get('rho') is not None else None,
        )
    
    @property
    def money(self) -> float | None:
        """
        if ndigits=0 is not provided, the return type will be int. 
        """
        if isinstance(self.last, float) and isinstance(self.open_interest, float):
            round_money = round(self.last * self.open_interest * 100.0, ndigits=0)
            return round_money
        else:
            return None


def get_close_price(symbol: str) -> float | None:

    ts = TimeSeries(key=API_KEY)
    data_dict, meta = ts.get_daily(symbol=symbol)
    
    td, ohlcv_dict: tuple[Any, dict[str, str]] = list(data_dict.items())[0]

    close_price = ohlcv_dict.get('4. close')
    
    # Get the most recent date's closing price
    #latest_date = list(data.keys())[0]
    #previous_close = data[latest_date]['4. close']
    #print(f"Previous Close ({latest_date}): ${previous_close}")

    return close_price


def get_cap(symbol: str) -> float | None:

    fd = FundamentalData(key=API_KEY)
    
    overview, _ = fd.get_company_overview(symbol=symbol)
    
    cap = overview["MarketCapitalization"]

    return readf(cap)


def get_hist_option_data(symbol:str) -> tuple[list, list]:
    """
    {'endpoint': 'Historical Options', 'message': 'success', 'data': [dict with all values are str]}

    DEPENDS: 

    USED BY: 
    """
    url = f'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol={symbol}&apikey=demo' 

    try:
        r = requests.get(url) 

        # .json() parses JSON body into Python dict
        data: dict[str, str | list[dict[str, str]]] = r.json()

    except Exception as e:
        print(e)
        return None, None

    # print(data.keys())

    # print(data.get('endpoint'))
    # print(data.get('message'))
    # print(data.get('Information'))
    # print(type(data))

    return data


def get_option_positions(symbol:str) -> tuple[list, list]:
    """
    
    """
    
    data: dict = get_hist_option_data('IBM') 

    option_list: list[dict[str, str]] = data.get('data')

    position_list: list[OptionPosition] = [OptionPosition.from_dict(x) for x in option_list]

    
    call_positions: list[OptionPosition] = [x for x in position_list if x.type == 'call']
    put_positions: list[OptionPosition] = [x for x in position_list if x.type == 'put']
    
    call_money_list: list[float] = [ x.money for x in call_positions if isinstance(x.money, float)]
    put_money_list: list[float] = [ x.money for x in put_positions if isinstance(x.money, float)]

    call_money: float = sum(call_money_list)
    
    put_money: float = sum(put_money_list)
    
    total_money: float = call_money + put_money

    print(call_money)
    

    call_oi: list[float] = sum([ x.open_interest for x in call_positions if isinstance(x.open_interest, float)])
    put_oi: list[float] = sum([ x.open_interest for x in put_positions if isinstance(x.open_interest, float)])

    sleep(1)

    close_price: float | None = get_close_price(symbol)

    sleep(2)    

    cap: float | None = get_cap(symbol)


    call_pct = call_money / cap
    
    put_pct = put_money / cap
    
    call_ratio = call_money / total_money
    
    put_ratio = put_money / total_money
    
    call_itm_premiums = sum([ x.money for x in call_positions if x.strike <= close_price and isinstance(x.money, float)])

    call_otm_premiums = sum([ x.money for x in call_positions if x.strike > close_price and isinstance(x.money, float)])

    put_itm_premiums = sum([ x.money for x in put_positions if x.strike >= close_price and isinstance(x.money, float)])

    put_otm_premiums = sum([ x.money for x in put_positions if x.strike < close_price and isinstance(x.money, float)])
    
    call_itm_ratio = call_itm_premiums / call_money
    call_otm_ratio = call_otm_premiums / call_money

    put_itm_ratio = put_itm_premiums / put_money
    put_otm_ratio = put_otm_premiums / put_money


    print(call_pct)
    print(put_pct)
    
    print(call_ratio)
    print(put_ratio)
    

    print(call_itm_ratio)
    print(call_otm_ratio)
    
    print(put_itm_ratio)
    print(put_otm_ratio)
    
    
    print(call_oi)
    print(put_oi)





    
if __name__ == '__main__':
    #get_option_positions('IBM')
    #get_cap('IBM')
    x = get_close_price('IBM')
    print(x)
    