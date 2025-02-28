from datetime import datetime
from unittest.mock import (
    AsyncMock,
    MagicMock,
)

from src.product_service.models import Lob
from src.product_service.repositories.lob import LobRepository


class TestLobRepository:
    async def test_insert_lob_repository(
        self,
        mock_async_session: AsyncMock,
        lob_repository: LobRepository,
        lob_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(scalar_one=lambda: 1)

        result = await lob_repository.insert(data=lob_data)
        assert result == 1

    async def test_get_one_lob_repository_found(
        self,
        mock_async_session: AsyncMock,
        lob_repository: LobRepository,
        lob_data: dict[str, str | int | datetime],
        returning_lob_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Lob(**returning_lob_data)
        )

        result = await lob_repository.get_one(
            filters={
                "id": 1,
            },
        )
        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == lob_data

    async def test_get_one_lob_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        lob_repository: LobRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await lob_repository.get_one(
            filters={
                "id": 999,
            },
        )

        assert result is None

    async def test_get_all_lob_repository_found(
        self,
        mock_async_session: AsyncMock,
        lob_repository: LobRepository,
        returning_lob_data_list: list[dict[str, str | int | datetime]],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            all=lambda: [(Lob(**data),) for data in returning_lob_data_list]
        )

        result = await lob_repository.get_all({})

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2

    async def test_get_all_lob_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        lob_repository: LobRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(all=lambda: [])

        result = await lob_repository.get_all({})

        assert len(result) == 0

    async def test_update_lob_repository_found(
        self,
        mock_async_session: AsyncMock,
        lob_repository: LobRepository,
        lob_data: dict[str, str | int | datetime],
        returning_lob_data: dict[str, str | int | datetime],
    ) -> None:
        lob_data.update({"name": "NAME"})
        returning_lob_data.update({"name": "NAME"})

        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Lob(**returning_lob_data)
        )

        result = await lob_repository.update(
            filters={
                "id": 1,
            },
            data={
                "name": "NAME",
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == lob_data

    async def test_update_lob_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        lob_repository: LobRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None,
        )

        result = await lob_repository.update(
            filters={
                "id": 999,
            },
            data={
                "name": "NAME",
            },
        )

        assert result is None

    async def test_delete_lob_repository_found(
        self,
        mock_async_session: AsyncMock,
        lob_repository: LobRepository,
        lob_data: dict[str, str | int | datetime],
        returning_lob_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Lob(**returning_lob_data)
        )

        result = await lob_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == lob_data

    async def test_delete_lob_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        lob_repository: LobRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await lob_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is None
