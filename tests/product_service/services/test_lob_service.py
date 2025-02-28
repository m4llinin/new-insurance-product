from unittest.mock import (
    AsyncMock,
    MagicMock,
)

from src.product_service.services.lob import LobService


class TestLobService:
    async def test_add_lob_success(
        self,
        lob_service: LobService,
        mock_product_uow: AsyncMock,
    ) -> None:
        test_data = {"name": "Test LOB", "description": "Test Description"}
        expected_id = 42

        mock_product_uow.lobs.insert.return_value = expected_id

        result = await lob_service.add(test_data)

        mock_product_uow.lobs.insert.assert_awaited_once_with(test_data)
        mock_product_uow.commit.assert_awaited_once()
        assert result == expected_id

    async def test_get_lobs_success(
        self,
        lob_service: LobService,
        mock_product_uow: AsyncMock,
    ) -> None:
        mock_lob = MagicMock(model_dump=lambda: {"id": 1, "name": "LOB1"})
        mock_product_uow.lobs.get_all.return_value = [mock_lob]

        result = await lob_service.get_lobs()

        mock_product_uow.lobs.get_all.assert_awaited_once_with({})
        assert result == [{"id": 1, "name": "LOB1"}]

    async def test_get_lobs_empty(
        self,
        lob_service: LobService,
        mock_product_uow: AsyncMock,
    ) -> None:
        mock_product_uow.lobs.get_all.return_value = []
        result = await lob_service.get_lobs()
        assert result == []
