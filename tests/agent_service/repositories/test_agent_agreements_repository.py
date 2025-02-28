from unittest.mock import (
    AsyncMock,
    MagicMock,
)

from src.agent_service.models import AgentAgreements
from src.agent_service.repositories.agent_agreements import AgentAgreementsRepository


class TestAgentAgreementsRepository:
    async def test_insert_agent_agreements_repository(
        self,
        mock_async_session: AsyncMock,
        agent_agreements_repository: AgentAgreementsRepository,
        agent_agreements_data: dict[str, str | int | float],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(scalar_one=lambda: 1)

        result = await agent_agreements_repository.insert(data=agent_agreements_data)
        assert result == 1

    async def test_get_one_agent_agreements_repository_found(
        self,
        mock_async_session: AsyncMock,
        agent_agreements_repository: AgentAgreementsRepository,
        agent_agreements_data: dict[str, str | int | float],
        returning_agent_agreements_data: dict[str, str | int | float],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: AgentAgreements(
                **returning_agent_agreements_data
            )
        )

        result = await agent_agreements_repository.get_one(
            filters={
                "id": 1,
            },
        )
        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == agent_agreements_data

    async def test_get_one_agent_agreements_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        agent_agreements_repository: AgentAgreementsRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await agent_agreements_repository.get_one(
            filters={
                "id": 999,
            },
        )

        assert result is None

    async def test_get_all_agent_agreements_repository_found(
        self,
        mock_async_session: AsyncMock,
        agent_agreements_repository: AgentAgreementsRepository,
        returning_agent_agreements_data_list: list[dict[str, str | int | float]],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            all=lambda: [
                (AgentAgreements(**data),)
                for data in returning_agent_agreements_data_list
            ]
        )

        result = await agent_agreements_repository.get_all({})

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2

    async def test_get_all_agent_agreements_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        agent_agreements_repository: AgentAgreementsRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(all=lambda: [])

        result = await agent_agreements_repository.get_all({})

        assert len(result) == 0

    async def test_update_agent_agreements_repository_found(
        self,
        mock_async_session: AsyncMock,
        agent_agreements_repository: AgentAgreementsRepository,
        agent_agreements_data: dict[str, str | int | float],
        returning_agent_agreements_data: dict[str, str | int | float],
    ) -> None:
        agent_agreements_data.update({"rate": 128.4})
        returning_agent_agreements_data.update({"rate": 128.4})

        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: AgentAgreements(
                **returning_agent_agreements_data
            )
        )

        result = await agent_agreements_repository.update(
            filters={
                "id": 1,
            },
            data={
                "rate": 128.4,
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == agent_agreements_data

    async def test_update_agent_agreements_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        agent_agreements_repository: AgentAgreementsRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None,
        )

        result = await agent_agreements_repository.update(
            filters={
                "id": 999,
            },
            data={
                "rate": 128.4,
            },
        )

        assert result is None

    async def test_delete_agent_agreements_repository_found(
        self,
        mock_async_session: AsyncMock,
        agent_agreements_repository: AgentAgreementsRepository,
        agent_agreements_data: dict[str, str | int | float],
        returning_agent_agreements_data: dict[str, str | int | float],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: AgentAgreements(
                **returning_agent_agreements_data
            )
        )

        result = await agent_agreements_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == agent_agreements_data

    async def test_delete_agent_agreements_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        agent_agreements_repository: AgentAgreementsRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await agent_agreements_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is None
