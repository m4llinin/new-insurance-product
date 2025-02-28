from datetime import datetime
from unittest.mock import (
    AsyncMock,
    MagicMock,
)

from src.auth_service.repostories.user import UserRepository
from src.auth_service.models.user import User


class TestUserRepository:
    async def test_insert_user_repository(
        self,
        mock_async_session: AsyncMock,
        user_repository: UserRepository,
        user_data: dict[str, str | int | bool],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(scalar_one=lambda: 1)

        result = await user_repository.insert(data=user_data)
        assert result == 1

    async def test_get_one_user_repository_found(
        self,
        mock_async_session: AsyncMock,
        user_repository: UserRepository,
        user_data: dict[str, str | int | bool],
        returning_user_data: dict[str, str | int | bool],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: User(**returning_user_data)
        )

        result = await user_repository.get_one(
            filters={
                "id": 1,
            },
        )
        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == user_data

    async def test_get_one_user_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        user_repository: UserRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await user_repository.get_one(
            filters={
                "id": 999,
            },
        )

        assert result is None

    async def test_update_user_repository_found(
        self,
        mock_async_session: AsyncMock,
        user_repository: UserRepository,
        user_data: dict[str, str | int | bool],
        returning_user_data: dict[str, str | int | bool],
    ) -> None:
        user_data.update({"is_active": False})
        returning_user_data.update({"is_active": False})

        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: User(**returning_user_data)
        )

        result = await user_repository.update(
            filters={
                "id": 1,
            },
            data={
                "is_active": False,
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == user_data

    async def test_update_user_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        user_repository: UserRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None,
        )

        result = await user_repository.update(
            filters={
                "id": 999,
            },
            data={
                "is_active": False,
            },
        )

        assert result is None

    async def test_delete_user_repository_found(
        self,
        mock_async_session: AsyncMock,
        user_repository: UserRepository,
        user_data: dict[str, str | int | bool],
        returning_user_data: dict[str, str | int | bool],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: User(**returning_user_data)
        )

        result = await user_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == user_data

    async def test_delete_user_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        user_repository: UserRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await user_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is None
