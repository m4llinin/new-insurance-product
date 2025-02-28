import pytest
from unittest.mock import AsyncMock

from src.auth_service.repostories.user import UserRepository


@pytest.fixture
def user_repository(
    mock_async_session: AsyncMock,
) -> UserRepository:
    return UserRepository(session=mock_async_session)
