"""
DEPENDS: pg_model.py

"""


# STANDARD LIB
import asyncio

from dataclasses import dataclass

from datetime import datetime, date, timedelta

from decimal import Decimal

import os

from pprint import pprint

from time import sleep

from typing import Any, Literal, Optional


# THIRD

from alpha_vantage.fundamentaldata import FundamentalData

from alpha_vantage.timeseries import TimeSeries

import asyncpg

from asyncpg import Record

import pandas as pd

from pandas import DataFrame

from pydantic import BaseModel, Field, validator

import requests

#CUSTOM

from pizzapy.pg_app.pg_model import fetch_latest_row_df

from batterypy.cal import get_trading_day, make_td_list

from batterypy.read import formatlarge, readf


from dimsumpy.av import get_cap, get_cap_dict, get_td_close, get_option_chain

from pizzapy.pg_app.pg_model import fetch_df


API_KEY = os.getenv('AV_API_KEY')






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
    call_money_ratio: Optional[float] = Field(None, ge=0, le=100.0, description="Call money as ratio of total")
    put_money_ratio: Optional[float] = Field(None, ge=0, le=100.0, description="Put money as ratio of total")
    
    # Premium ratios
    call_itm_premium_ratio: Optional[float] = Field(None, ge=0, le=100.0, description="Call ITM premium ratio")
    call_otm_premium_ratio: Optional[float] = Field(None, ge=0, le=100.0, description="Call OTM premium ratio")
    put_itm_premium_ratio: Optional[float] = Field(None, ge=0, le=100.0, description="Put ITM premium ratio")
    put_otm_premium_ratio: Optional[float] = Field(None, ge=0, le=100.0, description="Put OTM premium ratio")
    
    # Put/Call ratios
    call_pc: Optional[float] = Field(None, ge=0, description="Call put/call ratio")
    put_pc: Optional[float] = Field(None, ge=0, description="Put put/call ratio")
    half_call_money_point: Optional[float] = Field(None, ge=0, description="half call money point")
    half_put_money_point: Optional[float] = Field(None, ge=0, description="half put money point")
    
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
                if not (99.0 <= total <= 100.0):  # Allow small floating point errors
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










def calc_half_strike(option_positions: list[OptionPosition], half_money: float) -> float:
    
    accumulated_money: float = 0
    for x in option_positions:
        accumulated_money += x.money
        if accumulated_money > half_money:
            return x.strike
        
    return None


def calc_half_money_point(option_positions: list[OptionPosition], option_money: float, close_price: float) -> float:

    sorted_positions = sorted(option_positions, key=lambda x: x.strike)
    
    half_money: float = option_money / 2.0
    
    half_money_strike: float = calc_half_strike(sorted_positions, half_money)
    
    half_money_point: float = round(half_money_strike / close_price, ndigits=4)

    return half_money_point


async def get_close_cap_from_db(symbol: str, td: str | date) -> tuple[float, float]:
    
    #if isinstance(td, date):
    #    td: str = td.isoformat()
    
    table: str = 'stock_price'
    
    cmd = f"SELECT * FROM {table} WHERE symbol = '{symbol}' AND td = '{td}';"
    df = await fetch_df(cmd)
    
    close = df['close'].iloc[0]
    cap = df['cap'].iloc[0]
    
    return close, cap
    
    
        

async def make_option_ratio(symbol:str, td=None) -> OptionRatio:
    """
    # if isodate=None, this function will just return the latest option chain.
    
    # isodate can be 'YYYY-MM-DD' str, date object or datetime object.
    """
    
    if td is None:
        td, close_price = get_td_close(symbol)  # td is date obj, close_price is a float
        cap: float | None = get_cap(symbol)
    else:
        close_price, cap = await get_close_cap_from_db(symbol, td)

    
    option_list: list[dict[str, str]] = get_option_chain(symbol, isodate=td)

    position_list: list[OptionPosition] = [OptionPosition.from_dict(x) for x in option_list]

    call_positions: list[OptionPosition] = [x for x in position_list if x.type == 'call']
    put_positions: list[OptionPosition] = [x for x in position_list if x.type == 'put']
    
    call_money_list: list[float] = [ x.money for x in call_positions if isinstance(x.money, float)]
    put_money_list: list[float] = [ x.money for x in put_positions if isinstance(x.money, float)]

    call_money: float = sum(call_money_list)    

    put_money: float = sum(put_money_list)
    
    total_money: float = call_money + put_money
    
    call_oi: list[float] = sum([ x.open_interest for x in call_positions if isinstance(x.open_interest, float)])
    put_oi: list[float] = sum([ x.open_interest for x in put_positions if isinstance(x.open_interest, float)])

    t = datetime.now()

    half_call_money_point: float = calc_half_money_point(call_positions, call_money, close_price)
    half_put_money_point: float = calc_half_money_point(put_positions, put_money, close_price)
    
    

    cap_str=formatlarge(cap)

    call_pc = round(call_money / cap * 100.0, ndigits=4)
    
    put_pc = round(put_money / cap * 100.0, ndigits=4)
    
    call_money_ratio = round(call_money / total_money * 100.0, ndigits=2)
    
    put_money_ratio = round(put_money / total_money * 100.0, ndigits=2)
    
    call_itm_premiums = sum([ x.money for x in call_positions if x.strike <= close_price and isinstance(x.money, float)])

    call_otm_premiums = sum([ x.money for x in call_positions if x.strike > close_price and isinstance(x.money, float)])

    put_itm_premiums = sum([ x.money for x in put_positions if x.strike >= close_price and isinstance(x.money, float)])

    put_otm_premiums = sum([ x.money for x in put_positions if x.strike < close_price and isinstance(x.money, float)])
    
    call_itm_premium_ratio = round(call_itm_premiums / call_money * 100.0, ndigits=2)
    call_otm_premium_ratio = round(call_otm_premiums / call_money * 100.0, ndigits=2)

    put_itm_premium_ratio = round(put_itm_premiums / put_money * 100.0, ndigits=2)
    put_otm_premium_ratio = round(put_otm_premiums / put_money * 100.0, ndigits=2)

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
        half_call_money_point=half_call_money_point,
        half_put_money_point=half_put_money_point

    )

    pprint(option_obj)
    return option_obj



# Usage example with asyncpg
async def upsert_av_option(symbol: str, td=None) -> str:  # check Any type later
    """Insert an OptionRatio record into the database"""

    conn = await asyncpg.connect()

    option: OptionRatio = await make_option_ratio(symbol, td=td)

    result: str = await conn.execute('''
        INSERT INTO stock_option (
            t, td, symbol, cap_str, cap, price,
            call_money, put_money, call_oi, put_oi,
            call_money_ratio, put_money_ratio,
            call_itm_premium_ratio, call_otm_premium_ratio,
            put_itm_premium_ratio, put_otm_premium_ratio,
            call_pc, put_pc, half_call_money_point, half_put_money_point
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20)
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
            put_pc = EXCLUDED.put_pc,
            half_call_money_point = EXCLUDED.half_call_money_point,
            half_put_money_point = EXCLUDED.half_put_money_point
    ''', 
        option.t, option.td, option.symbol,
        option.cap_str, option.cap, option.price,
        option.call_money, option.put_money, option.call_oi, option.put_oi,
        option.call_money_ratio, option.put_money_ratio,
        option.call_itm_premium_ratio, option.call_otm_premium_ratio,
        option.put_itm_premium_ratio, option.put_otm_premium_ratio,
        option.call_pc, option.put_pc, 
        option.half_call_money_point, option.half_put_money_point
    )

    return result





async def upsert_av_options(stock_list: list[str], td=None) -> None:
    """
    DEPENDS:  upsert_av_option
    
    UPSERT SINGLE OPTION EXAMPLE:
        asyncio.run(upsert_av_options(['AMD'], isodate='2025-12-01'))
    
    
    """
    length: int = len(stock_list)
    
    for i, symbol in enumerate(stock_list, start=1):
        try:
            result: str = await upsert_av_option(symbol, td=td)

            output: str = f'{i} / {length} {symbol} {result}'
            print(output)

        except Exception as e:
            output: str = f'{i} / {length} {symbol} {e}'
            print(output)
            




async def upsert_interval_option(symbol: str, start=None, end=None, interval='monthly') -> None:  # check Any type later
    # still working
    
    if end is None:
        end = get_trading_day()
        
    if start is None:
        start = end - timedelta(days=365)

    await upsert_price(symbol=symbol, start=start, end=end) 

    td_list: list[date] = make_td_list(start=start, end=end, interval=interval)

    length: int = len(td_list)
    
    for i, td in enumerate(td_list, start=1):
        try:
            result: str = await upsert_av_option(symbol, td=td)

            output: str = f'{i} / {length} {symbol} {td} {result}'
            print(output)
            

        except Exception as e:
            output: str = f'{i} / {length} {symbol} {td} {e}'
            print(output)
    
    print(td_list)
            
###################
### STOCK PRICE ###
###################


async def upsert_price(symbol: str, start: str | date | None = None, end: str | date | None = None) -> None:
    
    if isinstance(start, str):
        start: date = date.fromisoformat(start)
    
    if isinstance(end, str):
        end: date = date.fromisoformat(end)
    
    table: str = 'stock_price'
    
    # defaults: asyncpg.create_pool(min_size=10, max_size=10)
    pool = await asyncpg.create_pool() 
    
    cap_dict: dict[str, dict[str, str | float | date | None]] = get_cap_dict(symbol)
    
    # ['symbol', 'td', 'close', 'adjclose', 'shares', 'cap']
    column_list: list[str] = list(next(iter(cap_dict.values())).keys())
    
    columns: str = ', '.join(column_list)
    
    placeholders: str = ', '.join(f'${i+1}' for i in range(len(column_list)))
    
    update_cols: list[str] = [c for c in column_list if c not in ('symbol', 'td')]
    
    update_clause: str = ', '.join(f'{c} = EXCLUDED.{c}' for c in update_cols)
    
    if start and end:
        rows: tuple[str, date, float, float, float, float] = [tuple(v.values()) for k, v in cap_dict.items() if date.fromisoformat(k) >= start and date.fromisoformat(k) <= end]
    elif start:
        rows: tuple[str, date, float, float, float, float] = [tuple(v.values()) for k, v in cap_dict.items() if date.fromisoformat(k) >= start]
    elif end:
        rows: tuple[str, date, float, float, float, float] = [tuple(v.values()) for k, v in cap_dict.items() if date.fromisoformat(k) <= end]
    else:
        rows: tuple[str, date, float, float, float, float] = [tuple(v.values()) for _, v in cap_dict.items()]
    
    
    async with pool.acquire() as conn:
        await conn.executemany(f'''
            INSERT INTO {table} ({columns}) 
            VALUES ({placeholders})
            ON CONFLICT (symbol, td) DO UPDATE SET {update_clause};''',
            rows
        )


async def upsert_prices(stock_list: list[str], start=None, end=None) -> None:
    """
    DEPENDS:  upsert_price
    
    UPSERT SINGLE STOCK:
        asyncio.run(upsert_prices(['AMD']))
        
        
    """
    length: int = len(stock_list)

    for i, symbol in enumerate(stock_list, start=1):
        try:
            result = await upsert_price(symbol, start=start, end=end)

            output: str = f'SUCCESS {i} / {length} {symbol} {result}'

            print(output)

        except Exception as e:
            error_output: str = f'ERROR {i} / {length} {symbol} {e}'
            print(error_output)


### END OF STOCK PRICE ###



async def main() -> None:

    await upsert_price('META', start='2026-01-01')





    
if __name__ == "__main__":
    
    #asyncio.run(upsert_interval_option('TSM', interval='fortnite'))
    asyncio.run(upsert_av_option('QBTS', td='2025-04-18'))
