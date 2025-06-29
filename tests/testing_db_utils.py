import os

from src.core.db_utils import DatabaseHelper

TEST_DB_URL = os.getenv("TEST_DB_URL")

test_db_helper = DatabaseHelper(
    url=TEST_DB_URL,
    echo=False,
    echo_pool=False,
    pool_size=5,
    max_overflow=10,
)
