from unittest.mock import MagicMock, patch, AsyncMock

import pytest

from src.product_service.services.metafield import MetaFieldService


class TestMetafieldService:
    async def test_get_meta_fields_success(
        self,
        metafield_service: MetaFieldService,
        mock_product_uow: AsyncMock,
    ) -> None:
        mock_meta = MagicMock(model_dump=lambda: {"id": 1, "key": "color"})
        mock_product_uow.meta_fields.get_all.return_value = [mock_meta]

        result = await metafield_service.get_meta_fields()

        mock_product_uow.meta_fields.get_all.assert_awaited_once_with({})
        assert result == [{"id": 1, "key": "color"}]

    async def test_get_meta_fields_empty(
        self,
        metafield_service: MetaFieldService,
        mock_product_uow: AsyncMock,
    ) -> None:
        mock_product_uow.meta_fields.get_all.return_value = []
        result = await metafield_service.get_meta_fields()
        assert result == []

    async def test_insert_meta_fields_success(
        self,
        metafield_service: MetaFieldService,
        mock_product_uow: AsyncMock,
    ) -> None:
        test_data = [{"key": "color"}, {"key": "size"}]
        mock_product_uow.meta_fields.insert.return_value = 42

        with patch.object(
            metafield_service, "insert_meta_field", AsyncMock(side_effect=[1, 2])
        ):
            result = await metafield_service.insert_meta_fields(test_data)

        assert result == [1, 2]

    async def test_insert_new_meta_field(
        self,
        metafield_service: MetaFieldService,
        mock_product_uow: AsyncMock,
    ) -> None:
        test_data = {"key": "color", "value": "red"}
        mock_product_uow.meta_fields.get_one.return_value = None
        mock_product_uow.meta_fields.insert.return_value = 42

        result = await metafield_service.insert_meta_field(test_data)

        mock_product_uow.meta_fields.insert.assert_awaited_once_with(test_data)
        mock_product_uow.commit.assert_awaited_once()
        assert result == 42

    async def test_insert_existing_meta_field(
        self,
        metafield_service: MetaFieldService,
        mock_product_uow: AsyncMock,
    ) -> None:
        test_data = {"key": "color"}
        mock_meta = MagicMock(id=1)
        mock_product_uow.meta_fields.get_one.return_value = mock_meta

        result = await metafield_service.insert_meta_field(test_data)

        assert result == 1

    async def test_get_metafield_rates_with_possible_values(
        self,
        metafield_service: MetaFieldService,
        mock_product_uow: AsyncMock,
    ) -> None:
        meta_fields = [{"id": 1, "value": "red"}]
        mock_meta = MagicMock(
            possible_values=["red", "blue"],
            coefficients=[1.2, 0.8],
            constant_coefficient=None,
        )
        mock_product_uow.meta_fields.get_one.return_value = mock_meta

        result = await metafield_service.get_metafield_rates(meta_fields)
        assert result == [1.2]

    async def test_get_metafield_rates_with_constant(
        self,
        metafield_service: MetaFieldService,
        mock_product_uow: AsyncMock,
    ) -> None:
        meta_fields = [{"id": 1, "value": "XL"}]
        mock_meta = MagicMock(possible_values=[], constant_coefficient=1.5)
        mock_product_uow.meta_fields.get_one.return_value = mock_meta

        result = await metafield_service.get_metafield_rates(meta_fields)
        assert result == [1.5]

    async def test_get_metafield_rates_not_found(
        self,
        metafield_service: MetaFieldService,
        mock_product_uow: AsyncMock,
    ) -> None:
        meta_fields = [{"id": 999, "value": "test"}]
        mock_product_uow.meta_fields.get_one.return_value = None

        with pytest.raises(ValueError, match="Metafield 999 not found"):
            await metafield_service.get_metafield_rates(meta_fields)
