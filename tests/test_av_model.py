
# THIRD PARTY LIBS
from asyncpg import Record

import pytest

from pizzapy.av_app.av_model import get_cap, get_close_price


@pytest.mark.asyncio
async def test_get_cap():
    cap = get_cap('NVDA')
    assert cap > 4_000_000_000_000.0
    assert isinstance(cap, float)

@pytest.mark.asyncio
async def test_get_close_price():
    t = get_close_price('NVDA')
    td = t[0]
    close_price = t[1]
    assert close_price > 100.0
    assert isinstance(td, str)
    assert isinstance(close_price, float)

