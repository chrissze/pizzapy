
# THIRD PARTY LIBS
from asyncpg import Record

import pytest

from pizzapy.av_app.av_model import get_cap, get_last_price




async def test_get_cap():
    assert get_cap('NVDA') > 4_000_000_000_000.0

async def test_get_last_price():
    assert get_last_price('NVDA') > 100.0

