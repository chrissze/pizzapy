# STANDARD LIB
import os

from time import sleep


# THIRD PARTY LIBS
from asyncpg import Record

import pytest




def test_api_key():
    api_key = os.getenv('AV_API_KEY')
    assert api_key[:2] == '2L'

