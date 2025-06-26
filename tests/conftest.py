import pytest

from src.core.config import settings


@pytest.fixture(scope="session")
def anyio_backend():
    return "anyio"


API_PREFIX = settings.api.prefix + settings.api.v1.prefix
