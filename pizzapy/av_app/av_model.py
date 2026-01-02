

import requests


from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Literal


@dataclass
class OptionPosition:
    contractID: str
    symbol: str
    expiration: date
    strike: Decimal
    type: Literal["call", "put"]
    last: float
    mark: Decimal
    bid: Decimal
    bid_size: int
    ask: Decimal
    ask_size: int
    volume: int
    open_interest: float
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
            strike=float(data["strike"]) if data.get('strike') is not None else None,
            type=data["type"] if data.get('type') is not None else None,
            last=float(data["last"]) if data.get('last') is not None else None,
            mark=Decimal(data["mark"]) if data.get('mark') is not None else None,
            bid=Decimal(data["bid"]) if data.get('bid') is not None else None,
            bid_size=int(data["bid_size"]) if data.get('bid_size') is not None else None,
            ask=Decimal(data["ask"]) if data.get('ask') is not None else None,
            ask_size=int(data["ask_size"]) if data.get('ask_size') is not None else None,
            volume=int(data["volume"]) if data.get('volume') is not None else None,
            open_interest=float(data["open_interest"]) if data.get('open_interest') is not None else None,
            date=date.fromisoformat(data["date"]) if data.get('date') is not None else None,
            implied_volatility=float(data["implied_volatility"]) if data.get('implied_volatility') is not None else None,
            delta=float(data["delta"]) if data.get('delta') is not None else None,
            gamma=float(data["gamma"]) if data.get('gamma') is not None else None,
            theta=float(data["theta"]) if data.get('theta') is not None else None,
            vega=float(data["vega"]) if data.get('vega') is not None else None,
            rho=float(data["rho"]) if data.get('rho') is not None else None,
        )
    
    @property
    def money(self) -> float:
        round_money = round(self.last * self.open_interest * 100.0)
        return round_money






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

    print(position_list)

    op0 = position_list[0]

    print(op0.money)

    call_positions: list[OptionPosition] = [x for x in position_list if x.type == 'call']
    put_positions: list[OptionPosition] = [x for x in position_list if x.type == 'put']
    
    call_money_list: list[float] = [ x.money for x in call_positions]
    put_money_list: list[float] = [ x.money for x in put_positions]

    call_money: float = sum(call_money_list)
    put_money: float = sum(put_money_list)

    print(call_money)
    print(put_money)





    
if __name__ == '__main__':
    get_option_positions('IBM') 