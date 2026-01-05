


# STANDARD LIB
import asyncio

from dataclasses import dataclass

from datetime import datetime, date

from decimal import Decimal

import os

from time import sleep

from typing import Any, Literal, Optional


# THIRD

from alpha_vantage.fundamentaldata import FundamentalData

from alpha_vantage.timeseries import TimeSeries

import asyncpg

from pydantic import BaseModel, Field, validator

import requests

#CUSTOM
from batterypy.string.read import formatlarge, readf



class OptionRatio(BaseModel):
    """
    Pydantic model for stock option data with validation.
    Represents options market sentiment and money flow metrics.
    """
    # Primary identifiers
    option_id: Optional[int] = Field(None, description="Auto-generated ID")
    t: Optional[datetime] = Field(None, description="Timestamp of data collection")
    td: date = Field(..., description="Trading date (part of primary key)")
    symbol: str = Field(..., min_length=1, max_length=10, description="Stock ticker symbol")
    
    # Market cap data
    cap_str: Optional[str] = Field(None, max_length=15, description="Market cap string representation")
    cap: Optional[float] = Field(None, ge=0, description="Market capitalization")
    
    # Price and money flow
    price: Optional[float] = Field(None, gt=0, description="Current stock price")
    call_money: Optional[float] = Field(None, ge=0, description="Total call option money flow")
    put_money: Optional[float] = Field(None, ge=0, description="Total put option money flow")
    
    # Open interest
    call_oi: Optional[float] = Field(None, ge=0, description="Call open interest")
    put_oi: Optional[float] = Field(None, ge=0, description="Put open interest")
    
    # Money ratios
    call_money_ratio: Optional[float] = Field(None, ge=0, le=1, description="Call money as ratio of total")
    put_money_ratio: Optional[float] = Field(None, ge=0, le=1, description="Put money as ratio of total")
    
    # Premium ratios
    call_itm_premium_ratio: Optional[float] = Field(None, ge=0, le=1, description="Call ITM premium ratio")
    call_otm_premium_ratio: Optional[float] = Field(None, ge=0, le=1, description="Call OTM premium ratio")
    put_itm_premium_ratio: Optional[float] = Field(None, ge=0, le=1, description="Put ITM premium ratio")
    put_otm_premium_ratio: Optional[float] = Field(None, ge=0, le=1, description="Put OTM premium ratio")
    
    # Put/Call ratios
    call_pc: Optional[float] = Field(None, ge=0, description="Call put/call ratio")
    put_pc: Optional[float] = Field(None, ge=0, description="Put put/call ratio")
    
    @validator('symbol')
    def normalize_symbol(cls, v):
        """Normalize ticker symbol to uppercase and strip whitespace"""
        if v:
            return v.upper().strip()
        return v
    
    @validator('td', pre=True)
    def parse_trade_date(cls, v):
        """Parse trading date from various formats"""
        if isinstance(v, date):
            return v
        if isinstance(v, datetime):
            return v.date()
        if isinstance(v, str):
            # Try common date formats
            for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%m/%d/%Y']:
                try:
                    return datetime.strptime(v, fmt).date()
                except ValueError:
                    continue
        return v
    
    @validator('t', pre=True)
    def parse_timestamp(cls, v):
        """Parse timestamp from various formats"""
        if v is None or isinstance(v, datetime):
            return v
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                pass
        return v
    
    @validator('call_money_ratio', 'put_money_ratio')
    def validate_money_ratios(cls, v, values):
        """Ensure money ratios sum to approximately 1.0"""
        if v is not None and 'call_money_ratio' in values and 'put_money_ratio' in values:
            call_ratio = values.get('call_money_ratio')
            put_ratio = values.get('put_money_ratio')
            if call_ratio is not None and put_ratio is not None:
                total = call_ratio + put_ratio
                if not (0.99 <= total <= 1.01):  # Allow small floating point errors
                    # Warning: could raise ValueError if you want strict validation
                    pass
        return v
    
    @validator('cap')
    def validate_cap_positive(cls, v):
        """Ensure market cap is positive if provided"""
        if v is not None and v < 0:
            raise ValueError('Market cap cannot be negative')
        return v
    
    class Config:
        # Enable validation on assignment
        validate_assignment = True
        
        # Allow datetime objects
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
        }
        
        # Example for documentation
        schema_extra = {
            "example": {
                "td": "2024-01-05",
                "symbol": "AAPL",
                "cap_str": "3.0T",
                "cap": 3000000000000,
                "price": 185.50,
                "call_money": 1500000000,
                "put_money": 800000000,
                "call_oi": 500000,
                "put_oi": 300000,
                "call_money_ratio": 0.65,
                "put_money_ratio": 0.35,
                "call_pc": 1.67,
                "put_pc": 0.60
            }
        }


# Usage example with asyncpg
async def upsert_option_ratio(symbol: str):
    """Insert an OptionRatio record into the database"""

    conn = await asyncpg.connect()

    option = get_option_ratio(symbol)

    await conn.execute('''
        INSERT INTO stock_option (
            t, td, symbol, cap_str, cap, price,
            call_money, put_money, call_oi, put_oi,
            call_money_ratio, put_money_ratio,
            call_itm_premium_ratio, call_otm_premium_ratio,
            put_itm_premium_ratio, put_otm_premium_ratio,
            call_pc, put_pc
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18)
        ON CONFLICT (symbol, td) DO UPDATE SET
            t = EXCLUDED.t,
            cap_str = EXCLUDED.cap_str,
            cap = EXCLUDED.cap,
            price = EXCLUDED.price,
            call_money = EXCLUDED.call_money,
            put_money = EXCLUDED.put_money,
            call_oi = EXCLUDED.call_oi,
            put_oi = EXCLUDED.put_oi,
            call_money_ratio = EXCLUDED.call_money_ratio,
            put_money_ratio = EXCLUDED.put_money_ratio,
            call_itm_premium_ratio = EXCLUDED.call_itm_premium_ratio,
            call_otm_premium_ratio = EXCLUDED.call_otm_premium_ratio,
            put_itm_premium_ratio = EXCLUDED.put_itm_premium_ratio,
            put_otm_premium_ratio = EXCLUDED.put_otm_premium_ratio,
            call_pc = EXCLUDED.call_pc,
            put_pc = EXCLUDED.put_pc
    ''', 
        option.t, option.td, option.symbol,
        option.cap_str, option.cap, option.price,
        option.call_money, option.put_money, option.call_oi, option.put_oi,
        option.call_money_ratio, option.put_money_ratio,
        option.call_itm_premium_ratio, option.call_otm_premium_ratio,
        option.put_itm_premium_ratio, option.put_otm_premium_ratio,
        option.call_pc, option.put_pc
    )



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
    
    td: str     # 'YYYY-MM-DD' '2026-01-02'
    ohlcv_dict: dict[str, str]
    td, ohlcv_dict = list(data_dict.items())[0]

    close_price = readf(ohlcv_dict.get('4. close'))
    
    # Get the most recent date's closing price
    #latest_date = list(data.keys())[0]
    #previous_close = data[latest_date]['4. close']
    #print(f"Previous Close ({latest_date}): ${previous_close}")

    #print(type(td))
    print(td, close_price)
    return td, close_price




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






def get_option_ratio(symbol:str) -> OptionRatio:
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
    t = datetime.now()
    td: str
    close_price: float | None
    td, close_price = get_close_price(symbol)

    sleep(2)    

    cap: float | None = get_cap(symbol)

    cap_str=formatlarge(cap)

    call_pc = call_money / cap * 100.0
    
    put_pc = put_money / cap * 100.0
    
    call_money_ratio = call_money / total_money
    
    put_money_ratio = put_money / total_money
    
    call_itm_premiums = sum([ x.money for x in call_positions if x.strike <= close_price and isinstance(x.money, float)])

    call_otm_premiums = sum([ x.money for x in call_positions if x.strike > close_price and isinstance(x.money, float)])

    put_itm_premiums = sum([ x.money for x in put_positions if x.strike >= close_price and isinstance(x.money, float)])

    put_otm_premiums = sum([ x.money for x in put_positions if x.strike < close_price and isinstance(x.money, float)])
    
    call_itm_premium_ratio = call_itm_premiums / call_money
    call_otm_premium_ratio = call_otm_premiums / call_money

    put_itm_premium_ratio = put_itm_premiums / put_money
    put_otm_premium_ratio = put_otm_premiums / put_money


    print(call_pc)
    print(put_pc)
    
    print(call_money_ratio)
    print(put_money_ratio)
    

    print(call_itm_premium_ratio)
    print(call_otm_premium_ratio)
    
    print(put_itm_premium_ratio)
    print(put_otm_premium_ratio)
    
    print(call_oi)
    print(put_oi)

    option_obj = OptionRatio(
        t=t,
        td=td,
        symbol=symbol,
        price=close_price,
        cap=cap,
        cap_str=cap_str,
        call_money=call_money, 
        put_money=put_money, 
        call_money_ratio=call_money_ratio, 
        put_money_ratio=put_money_ratio, 
        call_pc=call_pc,
        put_pc=put_pc,
        call_oi=call_oi,
        put_oi=put_oi,
        call_itm_premium_ratio=call_itm_premium_ratio,
        call_otm_premium_ratio=call_otm_premium_ratio,
        put_itm_premium_ratio=put_itm_premium_ratio,
        put_otm_premium_ratio=put_otm_premium_ratio,

    )

    return option_obj






# Example usage
if __name__ == "__main__":
    #op_obj = get_option_ratio('IBM')
    #print(op_obj)
    asyncio.run(upsert_option_ratio('IBM'))