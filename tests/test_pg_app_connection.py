"""

MAKE SURE I HAVE THE FOLLOWING ENV VARIABLES IN prompts.sh, THEY ARE asyncpg DEFAULT SYSTEM ENV VARIABLES FOR CONNECTION:

    export PGHOST='fuji.220122.xyz' or 'localhsot'  (UPDATE)
    export PGPORT=5432 
    export PGDATABASE='mydb'
    export PGUSER='postgres'
    export PGPASSWORD='hP'  (UPDATE)


"""

import asyncio
import os


import asyncpg

import pytest

def test_asyncpg_env() -> None:
    
    pghost = os.environ.get('PGHOST')

    pgport = os.environ.get('PGPORT')

    pgdatabase = os.environ.get('PGDATABASE')
    pguser = os.environ.get('PGUSER')

    assert pghost in ['localhost', 'fuji.220122.xyz'], f"Invalid PGHOST: {pghost} "
    assert pgport == '5432', f"Invalid PGPORT: {pgport} "
    assert pgdatabase == 'mydb', f"Invalid PGDATABASE: {pgdatabase} "
    assert pguser == 'postgres', f"Invalid PGDATABASE: {pguser} "



@pytest.mark.asyncio
async def test_pg_connection() -> None:
    
    e = None
    conn = None

    try: 
        pghost = os.environ.get('PGHOST')
    
        print(f'Connecting to a Posgresql database at {pghost} ...')

        
        conn = await asyncpg.connect()


        print(f'Successfully connected to a Posgresql database at {pghost}')

        # Filtered `Database Is Tempplate` is false: `WHERE datistemplate = false`
        databases = await conn.fetch("SELECT datname FROM pg_database;")

        print(databases)

    except Exception as e:
        print(e)
        assert e is None
    
    finally:
        assert conn is not None

        if conn is not None:
            await conn.close()


if __name__ == '__main__':
    asyncio.run(test_pg())

