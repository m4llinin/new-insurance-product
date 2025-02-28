import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.cache.helper import CacheHelper


@pytest.fixture
def mock_async_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture(scope="session", autouse=True)
async def mock_cache_helper() -> None:
    mock_client = AsyncMock()
    mock_client.get.return_value = None
    mock_client.set.return_value = None
    CacheHelper._client = mock_client
