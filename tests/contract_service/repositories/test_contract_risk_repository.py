from datetime import datetime
from unittest.mock import (
    AsyncMock,
    MagicMock,
)

from src.contract_service.models import ContractRisk
from src.contract_service.repositories.contract_risks import ContractRiskRepository


class TestContractRiskRepository:
    async def test_insert_contract_risk_repository(
        self,
        mock_async_session: AsyncMock,
        contract_risk_repository: ContractRiskRepository,
        contract_risk_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(scalar_one=lambda: 1)

        result = await contract_risk_repository.insert(data=contract_risk_data)
        assert result == 1

    async def test_get_one_contract_risk_repository_found(
        self,
        mock_async_session: AsyncMock,
        contract_risk_repository: ContractRiskRepository,
        contract_risk_data: dict[str, str | int | datetime],
        returning_contract_risk_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: ContractRisk(**returning_contract_risk_data)
        )

        result = await contract_risk_repository.get_one(
            filters={
                "id": 1,
            },
        )
        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == contract_risk_data

    async def test_get_one_contract_risk_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        contract_risk_repository: ContractRiskRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await contract_risk_repository.get_one(
            filters={
                "id": 999,
            },
        )

        assert result is None

    async def test_get_all_contract_risk_repository_found(
        self,
        mock_async_session: AsyncMock,
        contract_risk_repository: ContractRiskRepository,
        returning_contract_risk_data_list: list[dict[str, str | int | datetime]],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            all=lambda: [
                (ContractRisk(**data),) for data in returning_contract_risk_data_list
            ]
        )

        result = await contract_risk_repository.get_all({})

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2

    async def test_get_all_contract_risk_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        contract_risk_repository: ContractRiskRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(all=lambda: [])

        result = await contract_risk_repository.get_all({})

        assert len(result) == 0

    async def test_update_contract_risk_repository_found(
        self,
        mock_async_session: AsyncMock,
        contract_risk_repository: ContractRiskRepository,
        contract_risk_data: dict[str, str | int | datetime],
        returning_contract_risk_data: dict[str, str | int | datetime],
    ) -> None:
        contract_risk_data.update({"contract_id": 34})
        returning_contract_risk_data.update({"contract_id": 34})

        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: ContractRisk(**returning_contract_risk_data)
        )

        result = await contract_risk_repository.update(
            filters={
                "id": 1,
            },
            data={
                "contract_id": 34,
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == contract_risk_data

    async def test_update_contract_risk_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        contract_risk_repository: ContractRiskRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None,
        )

        result = await contract_risk_repository.update(
            filters={
                "id": 999,
            },
            data={
                "contract_id": 34,
            },
        )

        assert result is None

    async def test_delete_contract_risk_repository_found(
        self,
        mock_async_session: AsyncMock,
        contract_risk_repository: ContractRiskRepository,
        contract_risk_data: dict[str, str | int | datetime],
        returning_contract_risk_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: ContractRisk(**returning_contract_risk_data)
        )

        result = await contract_risk_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == contract_risk_data

    async def test_delete_contract_risk_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        contract_risk_repository: ContractRiskRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await contract_risk_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is None
