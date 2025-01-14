



import os
import pytest
from unittest.mock import patch, mock_open
from sqlalchemy.engine import Engine
from pizzapy.database_update.postgres_connection_model import execute_pandas_read

def test_config_json_file_exists():
    """
    Test to ensure /etc/config.json exists on the file system.
    """
    assert os.path.exists("/etc/config.json"), "The /etc/config.json file does not exist."


def test_database_connection():
    """
    result is np.int64(5)
    """
    df = execute_pandas_read('SELECT 2 + 3')
    result = df.iloc[-1, -1]
    assert result == 5