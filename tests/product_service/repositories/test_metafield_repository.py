from datetime import datetime
from unittest.mock import (
    AsyncMock,
    MagicMock,
)

from src.product_service.models import MetaField
from src.product_service.repositories.metafield import MetaFieldRepository


class TestMetaFieldRepository:
    async def test_insert_metafield_repository(
        self,
        mock_async_session: AsyncMock,
        metafield_repository: MetaFieldRepository,
        metafield_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(scalar_one=lambda: 1)

        result = await metafield_repository.insert(data=metafield_data)
        assert result == 1

    async def test_get_one_metafield_repository_found(
        self,
        mock_async_session: AsyncMock,
        metafield_repository: MetaFieldRepository,
        metafield_data: dict[str, str | int | datetime],
        returning_metafield_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: MetaField(**returning_metafield_data)
        )

        result = await metafield_repository.get_one(
            filters={
                "id": 1,
            },
        )
        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == metafield_data

    async def test_get_one_metafield_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        metafield_repository: MetaFieldRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await metafield_repository.get_one(
            filters={
                "id": 999,
            },
        )

        assert result is None

    async def test_get_all_metafield_repository_found(
        self,
        mock_async_session: AsyncMock,
        metafield_repository: MetaFieldRepository,
        returning_metafield_data_list: list[dict[str, str | int | datetime]],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            all=lambda: [(MetaField(**data),) for data in returning_metafield_data_list]
        )

        result = await metafield_repository.get_all({})

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2

    async def test_get_all_metafield_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        metafield_repository: MetaFieldRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(all=lambda: [])

        result = await metafield_repository.get_all({})

        assert len(result) == 0

    async def test_update_metafield_repository_found(
        self,
        mock_async_session: AsyncMock,
        metafield_repository: MetaFieldRepository,
        metafield_data: dict[str, str | int | datetime],
        returning_metafield_data: dict[str, str | int | datetime],
    ) -> None:
        metafield_data.update({"name": "NAME"})
        returning_metafield_data.update({"name": "NAME"})

        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: MetaField(**returning_metafield_data)
        )

        result = await metafield_repository.update(
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
        assert result == metafield_data

    async def test_update_metafield_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        metafield_repository: MetaFieldRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None,
        )

        result = await metafield_repository.update(
            filters={
                "id": 999,
            },
            data={
                "name": "NAME",
            },
        )

        assert result is None

    async def test_delete_metafield_repository_found(
        self,
        mock_async_session: AsyncMock,
        metafield_repository: MetaFieldRepository,
        metafield_data: dict[str, str | int | datetime],
        returning_metafield_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: MetaField(**returning_metafield_data)
        )

        result = await metafield_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == metafield_data

    async def test_delete_metafield_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        metafield_repository: MetaFieldRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await metafield_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is None
