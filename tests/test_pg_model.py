
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
    assert l >= 400


def test_get_sp_500():
    stocks: list[str] = get_sp_500()
    l = len(stocks)
    assert l >= 500


def test_get_nasdaq_100():
    stocks: list[str] = get_nasdaq_100()
    l = len(stocks)
    assert l >= 100


def test_get_sp_nasdaq():
    stocks: list[str] = get_sp_nasdaq()
    l = len(stocks)
    assert l >= 900


def test_get_option_traded():
    stocks: list[str] = get_option_traded()
    l = len(stocks)
    assert l >= 111900

