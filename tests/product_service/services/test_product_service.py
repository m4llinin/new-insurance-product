from unittest.mock import (
    MagicMock,
    AsyncMock,
)

from src.product_service.services.product import ProductService


class TestProductService:
    async def test_get_products_success(
        self,
        product_service: ProductService,
        mock_product_uow: AsyncMock,
    ) -> None:
        mock_product = MagicMock(
            meta_fields=[1, 2],
            model_dump=lambda: {"id": 1, "name": "Product1", "meta_fields": []},
        )
        mock_product_uow.products.get_all.return_value = [mock_product]
        result = await product_service.get_products()

        assert result == [
            {
                "id": 1,
                "name": "Product1",
                "meta_fields": [],
            }
        ]
        mock_product_uow.products.get_all.assert_awaited_once_with({})

    async def test_get_products_empty(
        self,
        product_service: ProductService,
        mock_product_uow: AsyncMock,
    ) -> None:
        mock_product_uow.products.get_all.return_value = []
        result = await product_service.get_products()
        assert result == []

    async def test_get_product_success(
        self,
        product_service: ProductService,
        mock_product_uow: AsyncMock,
    ) -> None:
        mock_product = MagicMock(
            meta_fields=[1],
            model_dump=lambda: {"id": 1, "name": "Product1", "meta_fields": []},
        )
        mock_product_uow.products.get_one.return_value = mock_product

        result = await product_service.get_product(1)

        assert result == {
            "id": 1,
            "name": "Product1",
            "meta_fields": [],
        }
