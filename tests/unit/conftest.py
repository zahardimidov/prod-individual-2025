import pytest
import logging
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app')))

os.environ['TEST_MODE'] = '1'
os.environ['ENGINE'] = 'sqlite+aiosqlite:///./database/database.db'

@pytest.fixture(autouse=True, scope="session")
def logger() -> logging.Logger:
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)

