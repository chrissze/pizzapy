
import os

from pizzapy.database_update.postgres_connection_model import execute_pandas_read, execute_psycopg_command, execute_psycopg_cursor_command

from pizzapy.pg_app import pg_cli


def test_config_json_file_exists():
    """
    Test to ensure /etc/config.json exists on the file system.
    """
    assert os.path.exists("/etc/config.json"), "The /etc/config.json file does not exist."


def test_pg_cli():
    """
    """

    assert pg_cli.main() == 'pg_cli'

