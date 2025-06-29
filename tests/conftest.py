import os

import pytest
from httpx import AsyncClient, ASGITransport

from src.core import DatabaseHelper
from src.core.config import settings
from src.main import main_app

TEST_DB_URL = os.getenv("TEST_DB_URL")
API_PREFIX = settings.api.prefix + settings.api.v1.prefix

test_db_helper = DatabaseHelper(url=TEST_DB_URL)


@pytest.fixture(scope='module')
def anyio_backend():
    return 'asyncio'


@pytest.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as ac:
        yield ac
