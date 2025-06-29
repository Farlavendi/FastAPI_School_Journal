import os

import pytest
from httpx import AsyncClient, ASGITransport

from src.core import db_helper
from src.core.config import settings
from src.core.models import Base
from src.main import main_app
from .testing_db_utils import test_db_helper

TEST_DB_URL = os.getenv("TEST_DB_URL")
API_PREFIX = settings.api.prefix + settings.api.v1.prefix


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope="function")
async def db_session():
    async with test_db_helper.engine.begin() as conn:
        await conn.begin_nested()

        session = test_db_helper.session_factory(bind=conn)
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest.fixture
async def async_client(db_session):
    async def _override():
        yield db_session

    main_app.dependency_overrides[db_helper.scoped_session_dependency] = _override

    async with AsyncClient(
        transport=ASGITransport(app=main_app),
        base_url=f"http://localhost",
    ) as ac:
        yield ac

    main_app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
async def reset_schema():
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def cleanup_test_db():
    yield
    await test_db_helper.dispose()
