from unittest.mock import MagicMock, AsyncMock

from src.contract_service.services.risk import RiskService


class TestRiskService:
    async def test_get_risks_success(
        self,
        risk_service: RiskService,
        mock_uow: AsyncMock,
    ) -> None:
        mock_risk = MagicMock(model_dump=lambda: {"id": 1, "name": "Test Risk"})
        mock_uow.risks.get_all.return_value = [mock_risk]

        result = await risk_service.get_risks()

        mock_uow.risks.get_all.assert_awaited_once_with({})
        assert result == [{"id": 1, "name": "Test Risk"}]

    async def test_get_risks_empty(
        self,
        risk_service: RiskService,
        mock_uow: AsyncMock,
    ) -> None:
        mock_uow.risks.get_all.return_value = []
        result = await risk_service.get_risks()
        assert result == []

    async def test_get_rates_success(
        self,
        risk_service: RiskService,
        mock_uow: AsyncMock,
    ) -> None:
        risk_ids = [1, 2]
        mock_risk1 = MagicMock(rate=0.5)
        mock_risk2 = MagicMock(rate=0.7)
        mock_uow.risks.get_one.side_effect = [mock_risk1, mock_risk2]

        result = await risk_service.get_rates(risk_ids)

        assert len(mock_uow.risks.get_one.await_args_list) == 2
        assert result == [0.5, 0.7]

    async def test_get_rates_with_missing_risk(
        self,
        risk_service: RiskService,
        mock_uow: AsyncMock,
    ) -> None:
        mock_uow.risks.get_one.return_value = None
        result = await risk_service.get_rates([999])
        assert len(result) == 0

    async def test_add_risk_success(
        self,
        risk_service: RiskService,
        mock_uow: AsyncMock,
    ) -> None:
        test_data = {"name": "New Risk", "rate": 0.3}
        mock_uow.risks.insert.return_value = 42

        result = await risk_service.add(test_data)

        mock_uow.risks.insert.assert_awaited_once_with(test_data)
        mock_uow.commit.assert_awaited_once()
        assert result == 42
