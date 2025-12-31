"""


Run pystest in terminal:

    (venv) $ cd ~/github/pizza_project
    (venv) $ python3 -m pytest -v pizzapy/tests/test_postgresql_database.py


"""

import os

from pizzapy.database_update.postgres_connection_model import execute_pandas_read, execute_psycopg_command, execute_psycopg_cursor_command


def test_config_json_file_exists():
    """
    Test to ensure /etc/config.json exists on the file system.
    """
    assert os.path.exists("/etc/config.json"), "The /etc/config.json file does not exist."


def test_sqlalchemy_connection():
    """
    result is np.int64(5)
    
    Notes: 
        execute_pandas_read() depends on make_sqlalchemy_engine() 
        and /etc/config.json, this test will make sure that make_sqlalchemy_engine() 
        will make a valid connection object. 

    """
    df = execute_pandas_read('SELECT 2 + 3')
    result = df.iloc[-1, -1]
    assert result == 5


def test_psycopg_connection():
    """
    Notes: 
        execute_psycopg_command() depends on make_psycopg_connection() 
        and /etc/config.json, this test will make sure that make_psycopg_connection()
        will make a valid connection object. 
    """ 
    result = execute_psycopg_command('SELECT 2 + 3')
    
    assert result == [(5,)]


def test_psycopg_current_database_is_mydb():
    """
    Notes: 
        execute_psycopg_cursor_command() depends on make_psycopg_connection() 
        and /etc/config.json, this test will make sure that psycopg has a 
        valid connection object. 
    """ 
    result = execute_psycopg_cursor_command('SELECT current_database()')
    
    assert result == [('mydb',)]