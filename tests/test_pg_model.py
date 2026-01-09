
# THIRD PARTY LIBS
from asyncpg import Record

import pytest

from pizzapy.pg_app.pg_model import get_current_db, get_tables, get_nasdaq_100, get_sp_400, get_sp_500, get_sp_nasdaq, get_option_traded

@pytest.mark.asyncio
async def test_get_current_db():
    db = await get_current_db()
    assert db == 'mydb', f'Wrong current db: {db}'


@pytest.mark.asyncio
async def test_get_tables():
    tables: list[Record] = await get_tables()
    
    assert isinstance(tables, list) 

### COMPUTER GENERATED STOCK LIST FILE ###

def test_get_sp_400():
    stocks: list[str] = get_sp_400()
    l = len(stocks)
    assert 395 <= l < 410
    assert 'AAL' in stocks
    assert 'GME' in stocks
    assert isinstance(stocks, list)
    assert isinstance(stocks[0], str)


def test_get_sp_500():
    stocks: list[str] = get_sp_500()
    l = len(stocks)
    assert 500 <= l < 510
    assert 'AMD' in stocks
    assert 'NVDA' in stocks
    assert isinstance(stocks, list)
    assert isinstance(stocks[0], str)


def test_get_nasdaq_100():
    stocks: list[str] = get_nasdaq_100()
    l = len(stocks)
    assert 100 <= l < 110
    assert 'AMD' in stocks
    assert 'NVDA' in stocks
    assert isinstance(stocks, list)
    assert isinstance(stocks[0], str)



def test_get_sp_nasdaq():
    # source code excludes bank stocks
    stocks: list[str] = get_sp_nasdaq()
    l = len(stocks)
    assert 800 <= l < 1000
    assert 'AMD' in stocks
    assert 'NVDA' in stocks


