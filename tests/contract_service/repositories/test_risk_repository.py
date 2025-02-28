from datetime import datetime
from unittest.mock import (
    AsyncMock,
    MagicMock,
)

from src.contract_service.models import Risk
from src.contract_service.repositories.risk import RiskRepository


class TestRiskRepository:
    async def test_insert_risk_repository(
        self,
        mock_async_session: AsyncMock,
        risk_repository: RiskRepository,
        risk_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(scalar_one=lambda: 1)

        result = await risk_repository.insert(data=risk_data)
        assert result == 1

    async def test_get_one_risk_repository_found(
        self,
        mock_async_session: AsyncMock,
        risk_repository: RiskRepository,
        risk_data: dict[str, str | int | datetime],
        returning_risk_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Risk(**returning_risk_data)
        )

        result = await risk_repository.get_one(
            filters={
                "id": 1,
            },
        )
        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == risk_data

    async def test_get_one_risk_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        risk_repository: RiskRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await risk_repository.get_one(
            filters={
                "id": 999,
            },
        )

        assert result is None

    async def test_get_all_risk_repository_found(
        self,
        mock_async_session: AsyncMock,
        risk_repository: RiskRepository,
        returning_risk_data_list: list[dict[str, str | int | datetime]],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            all=lambda: [
                (Risk(**data),) for data in returning_risk_data_list
            ]
        )

        result = await risk_repository.get_all({})

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2

    async def test_get_all_risk_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        risk_repository: RiskRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(all=lambda: [])

        result = await risk_repository.get_all({})

        assert len(result) == 0

    async def test_update_risk_repository_found(
        self,
        mock_async_session: AsyncMock,
        risk_repository: RiskRepository,
        risk_data: dict[str, str | int | datetime],
        returning_risk_data: dict[str, str | int | datetime],
    ) -> None:
        risk_data.update({"rate": 34.543})
        returning_risk_data.update({"rate": 34.543})

        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Risk(**returning_risk_data)
        )

        result = await risk_repository.update(
            filters={
                "id": 1,
            },
            data={
                "rate": 34.543,
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == risk_data

    async def test_update_risk_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        risk_repository: RiskRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None,
        )

        result = await risk_repository.update(
            filters={
                "id": 999,
            },
            data={
                "rate": 34.543,
            },
        )

        assert result is None

    async def test_delete_risk_repository_found(
        self,
        mock_async_session: AsyncMock,
        risk_repository: RiskRepository,
        risk_data: dict[str, str | int | datetime],
        returning_risk_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Risk(**returning_risk_data)
        )

        result = await risk_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == risk_data

    async def test_delete_risk_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        risk_repository: RiskRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await risk_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is None
