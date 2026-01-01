
# THIRD PARTY LIBS
from asyncpg import Record

import pytest

from pizzapy.pg_app.pg_model import get_current_db, get_tables

@pytest.mark.asyncio
async def test_get_current_db():
    db = await get_current_db()
    assert db == 'mydb', f'Wrong current db: {db}'


@pytest.mark.asyncio
async def test_get_tables():
    tables: list[Record] = await get_tables()
    
    assert isinstance(tables, list) 