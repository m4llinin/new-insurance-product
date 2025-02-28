import pytest
from unittest.mock import (
    MagicMock,
    AsyncMock,
)

from src.contract_service.services.contract_risks import ContractRiskService


class TestContractRiskService:
    async def test_add_contract_risk_success(
        self,
        contract_risk_service: ContractRiskService,
        mock_uow: AsyncMock,
    ) -> None:
        test_data = {"contract_id": 1, "risk_id": [2, 3]}
        expected_id = 42

        mock_uow.contract_risks.insert.return_value = expected_id

        result = await contract_risk_service.add_contract_risk(test_data)

        mock_uow.contract_risks.insert.assert_awaited_once_with(test_data)
        mock_uow.commit.assert_awaited_once()
        assert result == expected_id

    async def test_get_contract_risk_found(
        self,
        contract_risk_service: ContractRiskService,
        mock_uow: AsyncMock,
    ) -> None:
        contract_id = 1
        mock_risk = MagicMock(risk_id=[2, 3])
        mock_uow.contract_risks.get_one.return_value = mock_risk

        result = await contract_risk_service.get_contract_risk(contract_id)

        mock_uow.contract_risks.get_one.assert_awaited_once_with(
            {"contract_id": contract_id}
        )
        assert result == [2, 3]

    async def test_get_contract_risk_not_found(
        self,
        contract_risk_service: ContractRiskService,
        mock_uow: AsyncMock,
    ) -> None:
        contract_id = 999
        mock_uow.contract_risks.get_one.return_value = None

        with pytest.raises(ValueError) as exc_info:
            await contract_risk_service.get_contract_risk(contract_id)

        assert str(exc_info.value) == f"Contract risk not found: {contract_id}"

    async def test_cache_in_get_contract_risk(
        self,
        contract_risk_service: ContractRiskService,
        mock_uow: AsyncMock,
    ) -> None:
        contract_id = 1
        mock_risk = MagicMock(risk_id=[2, 3])
        mock_uow.contract_risks.get_one.return_value = mock_risk

        result = await contract_risk_service.get_contract_risk(contract_id)

        assert result == [2, 3]
        mock_uow.contract_risks.get_one.assert_awaited_once()
