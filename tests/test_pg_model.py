import pytest

from pizzapy.pg_app.pg_model import get_current_db

@pytest.mark.asyncio
async def test_get_current_db():
    assert await get_current_db() == 'mydb' 