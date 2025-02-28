from datetime import datetime
from unittest.mock import (
    AsyncMock,
    MagicMock,
)

from src.agent_service.models import Agent
from src.agent_service.repositories.agent import AgentRepository


class TestAgentRepository:
    async def test_insert_agent_repository(
        self,
        mock_async_session: AsyncMock,
        agent_repository: AgentRepository,
        agent_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(scalar_one=lambda: 1)

        result = await agent_repository.insert(data=agent_data)
        assert result == 1

    async def test_get_one_agent_repository_found(
        self,
        mock_async_session: AsyncMock,
        agent_repository: AgentRepository,
        agent_data: dict[str, str | int | datetime],
        returning_agent_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Agent(**returning_agent_data)
        )

        result = await agent_repository.get_one(
            filters={
                "id": 1,
            },
        )
        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == agent_data

    async def test_get_one_agent_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        agent_repository: AgentRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await agent_repository.get_one(
            filters={
                "id": 999,
            },
        )

        assert result is None

    async def test_get_all_agent_repository_found(
        self,
        mock_async_session: AsyncMock,
        agent_repository: AgentRepository,
        returning_agent_data_list: list[dict[str, str | int | datetime]],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            all=lambda: [(Agent(**data),) for data in returning_agent_data_list]
        )

        result = await agent_repository.get_all({})

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2

    async def test_get_all_agent_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        agent_repository: AgentRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(all=lambda: [])

        result = await agent_repository.get_all({})

        assert len(result) == 0

    async def test_update_agent_repository_found(
        self,
        mock_async_session: AsyncMock,
        agent_repository: AgentRepository,
        agent_data: dict[str, str | int | datetime],
        returning_agent_data: dict[str, str | int | datetime],
    ) -> None:
        agent_data.update({"ikp_id": 2})
        returning_agent_data.update({"ikp_id": 2})

        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Agent(**returning_agent_data)
        )

        result = await agent_repository.update(
            filters={
                "id": 1,
            },
            data={
                "ikp_id": 2,
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == agent_data

    async def test_update_agent_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        agent_repository: AgentRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None,
        )

        result = await agent_repository.update(
            filters={
                "id": 999,
            },
            data={
                "ikp_id": 2,
            },
        )

        assert result is None

    async def test_delete_agent_repository_found(
        self,
        mock_async_session: AsyncMock,
        agent_repository: AgentRepository,
        agent_data: dict[str, str | int | datetime],
        returning_agent_data: dict[str, str | int | datetime],
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: Agent(**returning_agent_data)
        )

        result = await agent_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is not None
        result = result.model_dump()
        assert result["id"] == 1
        result.pop("id")
        assert result == agent_data

    async def test_delete_agent_repository_not_found(
        self,
        mock_async_session: AsyncMock,
        agent_repository: AgentRepository,
    ) -> None:
        mock_async_session.execute.return_value = MagicMock(
            scalar_one_or_none=lambda: None
        )

        result = await agent_repository.delete(
            filters={
                "id": 1,
            },
        )

        assert result is None

    async def test_get_one_with_face_agent_repository_found(
        self,
        mock_async_session: AsyncMock,
        agent_repository: AgentRepository,
        returning_agent_data_with_face: dict[str, str | int | float | datetime],
    ) -> None:
        mock_result = MagicMock()
        mock_result.mappings.return_value.one.return_value = {
            "agent_id": 1,
            "Agent": MagicMock(
                to_dict=lambda: {
                    "id": 1,
                    "email": "example@email.com",
                    "face_id": 1,
                    "ikp_id": 1,
                    "date_create": datetime(2024, 1, 2, 23),
                    "date_begin": datetime(2024, 1, 2, 23),
                    "date_end": datetime(2024, 1, 3, 20),
                },
            ),
            "Face": MagicMock(
                to_dict=lambda: {
                    "id": 1,
                    "first_name": "VASYA",
                    "second_name": "PETROVICH",
                    "last_name": "MUROV",
                    "date_of_birth": datetime(2024, 1, 2),
                    "name": "OOO FOOTBALL",
                    "inn": 123213,
                },
            ),
            "ikp_name": "IKP_NAME",
            "AgentAgreements": MagicMock(
                to_dict=lambda: {
                    "id": 1,
                    "agent_id": 1,
                    "lob_id": 1,
                    "rate": 112.25,
                },
            ),
            "status": MagicMock(
                value="active",
            ),
            "type": MagicMock(
                value="legal",
            ),
        }

        mock_async_session.execute.return_value = mock_result

        result = await agent_repository.get_one_with_face(
            filters={
                "email": "email@example.com",
            },
        )

        assert result is not None
        assert result == returning_agent_data_with_face
