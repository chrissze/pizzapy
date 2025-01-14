import pytest

from pizzapy.database_update.postgres_connection_model import make_sqlalchemy_engine


# Test that the function raises a FileNotFoundError if the config file doesn't exist
def test_make_sqlalchemy_engine_missing_config_file():
    with pytest.raises(FileNotFoundError):
        make_sqlalchemy_engine()

