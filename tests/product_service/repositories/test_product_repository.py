from datetime import datetime
from unittest.mock import (
    AsyncMock,
    MagicMock,
)

from src.product_service.models import Product
from src.product_service.repositories.product import ProductRepository


class TestProductRepository:
    async def test_insert_product_repository(
        self,
        mock_async_session: AsyncMock,
        product_repository: ProductRepository,
        product_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(scalar_one=lambda: 1)

        result = await product_repository.insert(data=product_data)
        assert result == 1

    async def test_get_one_product_repository_found(
        self,
        mock_async_session: AsyncMock,
        product_repository: ProductRepository,
        product_data: dict[str, str | int | datetime],
        returning_product_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Product(**returning_product_data)
        )

        result = await product_repository.get_one(
            filters={
                "id": 1,
            },
        )
        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == product_data

    async def test_get_one_product_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        product_repository: ProductRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await product_repository.get_one(
            filters={
                "id": 999,
            },
        )

        assert result is None

    async def test_get_all_product_repository_found(
        self,
        mock_async_session: AsyncMock,
        product_repository: ProductRepository,
        returning_product_data_list: list[dict[str, str | int | datetime]],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            all=lambda: [(Product(**data),) for data in returning_product_data_list]
        )

        result = await product_repository.get_all({})

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2

    async def test_get_all_product_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        product_repository: ProductRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(all=lambda: [])

        result = await product_repository.get_all({})

        assert len(result) == 0

    async def test_update_product_repository_found(
        self,
        mock_async_session: AsyncMock,
        product_repository: ProductRepository,
        product_data: dict[str, str | int | datetime],
        returning_product_data: dict[str, str | int | datetime],
    ) -> None:
        product_data.update({"name": "NAME"})
        returning_product_data.update({"name": "NAME"})

        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Product(**returning_product_data)
        )

        result = await product_repository.update(
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
        assert result == product_data

    async def test_update_product_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        product_repository: ProductRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None,
        )

        result = await product_repository.update(
            filters={
                "id": 999,
            },
            data={
                "name": "NAME",
            },
        )

        assert result is None

    async def test_delete_product_repository_found(
        self,
        mock_async_session: AsyncMock,
        product_repository: ProductRepository,
        product_data: dict[str, str | int | datetime],
        returning_product_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Product(**returning_product_data)
        )

        result = await product_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == product_data

    async def test_delete_product_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        product_repository: ProductRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await product_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is None
