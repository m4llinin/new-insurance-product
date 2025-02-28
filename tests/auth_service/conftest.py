from annotated_types import T
import pytest
from unittest.mock import (
    AsyncMock,
    MagicMock,
    patch,
)

from src.auth_service.schemes.auth import AuthSchemeRequest
from src.auth_service.services.auth import AuthService
from src.auth_service.utils.jwt_helper import JWTHelper
from src.auth_service.utils.uow import AuthUOW


@pytest.fixture
def mock_config() -> MagicMock:
    config = MagicMock()
    config.auth.SECRET_KEY = "test_secret_key"
    config.auth.ALGORITHM = "HS256"
    config.auth.ACCESS_TOKEN_EXPIRE_MINUTES = 15
    config.auth.REFRESH_TOKEN_EXPIRE_DAYS = 30
    return config


@pytest.fixture
def jwt_helper(mock_config: MagicMock) -> JWTHelper:
    with patch("src.auth_service.utils.jwt_helper.Config", return_value=mock_config):
        return JWTHelper()


@pytest.fixture
async def auth_uow() -> AuthUOW:
    return AuthUOW()


@pytest.fixture
def mock_auth_uow() -> AsyncMock:
    uow = AsyncMock(spec=AuthUOW)
    uow.users = AsyncMock()
    return uow


@pytest.fixture
def auth_service(mock_auth_uow: AsyncMock) -> AuthService:
    return AuthService(mock_auth_uow)


@pytest.fixture
def credentials() -> AuthSchemeRequest:
    return AuthSchemeRequest(
        email="example@email.com",
        password="password",
    )


@pytest.fixture
def user_data() -> dict[str, str]:
    return {
        "email": "example@email.com",
        "hashed_password": "hashed_password",
        "role": "user",
        "is_active": False,
    }


@pytest.fixture
def returning_user_data() -> dict[str, str | int | bool]:
    return {
        "id": 1,
        "email": "example@email.com",
        "hashed_password": "hashed_password",
        "role": "user",
        "is_active": False,
    }
