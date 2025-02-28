from datetime import datetime
from unittest.mock import (
    AsyncMock,
    MagicMock,
)

from src.contract_service.schemes.contract import (
    ContractAddScheme,
    ContractFiltersScheme,
    PeriodScheme,
    CalculatePriceScheme,
)
from src.contract_service.services.contract import ContractService


class TestContractService:
    async def test_get_contracts_success(
        self,
        contract_service: ContractService,
        mock_uow: AsyncMock,
    ) -> None:
        mock_contract = MagicMock(model_dump=lambda: {"id": 1, "status": "SIGNED"})
        mock_uow.contracts.get_all.return_value = [mock_contract]
        filters = ContractFiltersScheme(agent_id=1, status="SIGNED")

        result = await contract_service.get_contracts(filters)

        mock_uow.contracts.get_all.assert_awaited_once_with(
            {
                "agent_id": 1,
                "status": "SIGNED",
            }
        )
        assert result == [{"id": 1, "status": "SIGNED"}]

    async def test_add_contract_success(
        self,
        contract_service: ContractService,
        mock_uow: AsyncMock,
    ) -> None:
        contract_data = ContractAddScheme(
            policy_price=1,
            agent_id=1,
            policy_holder_id=1,
            insured_personal_id=1,
            owner_id=1,
            risk_id=[1, 2],
            premium=1000,
            insurance_sum=50000,
            product_id=1,
            status="DRAFT",
            date_create=datetime(2024, 1, 1, 23, 49),
            date_sign=datetime(2024, 1, 1, 23, 49),
            date_begin=datetime(2024, 1, 1, 23, 49),
            date_end=datetime(2024, 1, 1, 23, 49),
        )
        mock_uow.contracts.insert.return_value = 1

        contract_id = await contract_service.add_contract(contract_data)

        mock_uow.contracts.insert.assert_awaited_once()
        assert contract_id == 1

    async def test_calculate_agent_premium(
        self,
        contract_service: ContractService,
    ) -> None:
        result = await contract_service.calculate_agent_premium(
            agent_rate=10.0, contract_price=1000
        )
        assert result["price"] == 100  # 10% от 1000
