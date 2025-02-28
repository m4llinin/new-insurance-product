import pytest
from unittest.mock import (
    AsyncMock,
    MagicMock,
)
from src.auth_service.services.auth import AuthService
from src.auth_service.schemes.auth import AuthSchemeRequest


@pytest.fixture
def token() -> str:
    return "valid_token"


class TestAuthService:
    async def test_register_user_success(
        self,
        auth_service: AuthService,
        mock_auth_uow: AsyncMock,
        credentials: AuthSchemeRequest,
    ) -> None:
        mock_auth_uow.users.get_one.return_value = None
        mock_auth_uow.users.insert.return_value = 1

        result = await auth_service.register_user(credentials)

        mock_auth_uow.users.get_one.assert_awaited_once_with(
            {
                "email": credentials.email,
            }
        )
        mock_auth_uow.users.insert.assert_awaited_once()
        mock_auth_uow.commit.assert_awaited_once()
        assert result is not None
        assert result["id"] == 1

    async def test_register_user_already_exists(
        self,
        auth_service: AuthService,
        mock_auth_uow: AsyncMock,
        credentials: AuthSchemeRequest,
    ) -> None:
        mock_auth_uow.users.get_one.return_value = MagicMock()

        with pytest.raises(ValueError, match="User already exists"):
            await auth_service.register_user(credentials)

    async def test_login_user_success(
        self,
        auth_service: AuthService,
        mock_auth_uow: AsyncMock,
        credentials: AuthSchemeRequest,
        returning_user_data: dict[str, str | int | bool],
    ) -> None:
        user_mock = MagicMock(**returning_user_data)
        mock_auth_uow.users.get_one.return_value = user_mock
        auth_service._pwd_helper.verify_password = MagicMock(return_value=True)

        result = await auth_service.login_user(credentials)

        mock_auth_uow.users.update.assert_awaited_once_with(
            filters={
                "id": 1,
            },
            data={
                "is_active": True,
            },
        )
        assert "access_token" in result
        assert "refresh_token" in result

    async def test_login_user_invalid_credentials(
        self,
        auth_service: AuthService,
        mock_auth_uow: AsyncMock,
        credentials: AuthSchemeRequest,
    ) -> None:
        mock_auth_uow.users.get_one.return_value = None

        with pytest.raises(ValueError, match="Invalid password or email"):
            await auth_service.login_user(credentials)

    async def test_logout_user_success(
        self,
        auth_service: AuthService,
        mock_auth_uow: AsyncMock,
        token: str,
    ) -> None:
        auth_service._jwt_helper.decode_and_check_token = MagicMock(
            return_value={
                "user_id": 1,
            }
        )
        user_mock = MagicMock(is_active=True)
        mock_auth_uow.users.get_one.return_value = user_mock

        result = await auth_service.logout_user(token)

        mock_auth_uow.users.update.assert_awaited_once_with(
            filters={
                "id": 1,
            },
            data={
                "is_active": False,
            },
        )
        assert result["id"] == 1

    async def test_refresh_token_success(
        self,
        auth_service: AuthService,
        mock_auth_uow: AsyncMock,
        token: str,
    ) -> None:
        auth_service._jwt_helper.decode_and_check_token = MagicMock(
            return_value={
                "user_id": 1,
            }
        )
        user_mock = MagicMock(
            id=1,
            email="example@email.com",
            is_active=True,
        )
        mock_auth_uow.users.get_one.return_value = user_mock
        auth_service._jwt_helper.create_token = MagicMock(
            return_value="new_access_token"
        )

        result = await auth_service.refresh_token(token)

        assert result["access_token"] == "new_access_token"

    async def test_get_current_user_success(
        self,
        auth_service: AuthService,
        mock_auth_uow: AsyncMock,
        token: str,
    ) -> None:
        auth_service._jwt_helper.decode_and_check_token = MagicMock(
            return_value={
                "user_id": 1,
            }
        )
        user_mock = MagicMock(
            is_active=True,
            email="example@email.com",
        )
        mock_auth_uow.users.get_one.return_value = user_mock

        result = await auth_service.get_current_user(token)

        assert result == "example@email.com"

    async def test_check_user_is_authorized_true(
        self,
        auth_service: AuthService,
        mock_auth_uow: AsyncMock,
        token: str,
    ) -> None:
        auth_service._jwt_helper.decode_and_check_token = MagicMock(
            return_value={
                "user_id": 1,
            }
        )
        user_mock = MagicMock(is_active=True)
        mock_auth_uow.users.get_one.return_value = user_mock

        result = await auth_service.check_user_is_authorized(token)

        assert result is True
