import pytest

from .conftest import async_client

pytestmark = pytest.mark.anyio


async def test_main(async_client):
    response = await async_client.get("/")
    assert response.status_code == 307
