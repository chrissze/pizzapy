
# THIRD PARTY LIBS
from asyncpg import Record

import pytest

from pizzapy.pg_app.pg_model import get_option_traded

def test_get_option_traded():
    # 5 minutes run time
    stocks: list[str] = get_option_traded()
    l = len(stocks)
    assert 2000 <= l < 5000
    assert 'AMD' in stocks
    assert 'NVDA' in stocks
    assert isinstance(stocks, list)
    assert isinstance(stocks[0], str)
