from datetime import datetime
from unittest.mock import (
    AsyncMock,
    MagicMock,
)

from src.contract_service.models import Contract
from src.contract_service.repositories.contract import ContractRepository


class TestContractRepository:
    async def test_insert_contract_repository(
        self,
        mock_async_session: AsyncMock,
        contract_repository: ContractRepository,
        contract_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(scalar_one=lambda: 1)

        result = await contract_repository.insert(data=contract_data)
        assert result == 1

    async def test_get_one_contract_repository_found(
        self,
        mock_async_session: AsyncMock,
        contract_repository: ContractRepository,
        contract_data: dict[str, str | int | datetime],
        returning_contract_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Contract(**returning_contract_data)
        )

        result = await contract_repository.get_one(
            filters={
                "id": 1,
            },
        )
        assert result is not None
        result = result.model_dump(exclude_none=True)
        assert result["id"] == 1
        result.pop("id")
        contract_data.pop("risk_id")
        assert result == contract_data

    async def test_get_one_contract_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        contract_repository: ContractRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await contract_repository.get_one(
            filters={
                "id": 999,
            },
        )

        assert result is None

    async def test_get_all_contract_repository_found(
        self,
        mock_async_session: AsyncMock,
        contract_repository: ContractRepository,
        returning_contract_data_list: list[dict[str, str | int | datetime]],
    ) -> None:
        mock_async_session.execute = AsyncMock()
        mock_result = MagicMock()
        mock_result.mappings.return_value = [
            {"Contract": Contract(**data)} for data in returning_contract_data_list
        ]
        mock_async_session.execute.return_value = mock_result

        result = await contract_repository.get_all({})

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2

    async def test_get_all_contract_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        contract_repository: ContractRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(all=lambda: [])

        result = await contract_repository.get_all({})

        assert len(result) == 0

    async def test_update_contract_repository_found(
        self,
        mock_async_session: AsyncMock,
        contract_repository: ContractRepository,
        contract_data: dict[str, str | int | datetime],
        returning_contract_data: dict[str, str | int | datetime],
    ) -> None:
        contract_data.update({"rate": 34.0})
        returning_contract_data.update({"rate": 34.0})

        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Contract(**returning_contract_data)
        )

        result = await contract_repository.update(
            filters={
                "id": 1,
            },
            data={
                "rate": 34.0,
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == contract_data

    async def test_update_contract_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        contract_repository: ContractRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None,
        )

        result = await contract_repository.update(
            filters={
                "id": 999,
            },
            data={
                "contract_id": 34,
            },
        )

        assert result is None

    async def test_delete_contract_repository_found(
        self,
        mock_async_session: AsyncMock,
        contract_repository: ContractRepository,
        contract_data: dict[str, str | int | datetime],
        returning_contract_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Contract(**returning_contract_data)
        )

        result = await contract_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == contract_data

    async def test_delete_contract_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        contract_repository: ContractRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await contract_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is None
