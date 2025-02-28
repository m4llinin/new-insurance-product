from datetime import datetime
from unittest.mock import AsyncMock
from src.agent_service.services.agent import AgentService


class TestAgentService:
    async def test_add_agent(
        self,
        agent_service: AgentService,
        mock_agent_uow: AsyncMock,
        agent_data: dict[str, str | int | datetime],
    ) -> None:
        mock_agent_uow.agents.insert.return_value = 1

        agent_id = await agent_service.add(agent=agent_data)

        mock_agent_uow.agents.insert.assert_awaited_once_with(agent_data)
        mock_agent_uow.commit.assert_awaited_once()
        assert agent_id == 1

    async def test_get_profile(
        self,
        agent_service: AgentService,
        mock_agent_uow: AsyncMock,
        returning_agent_data: dict[str, str | int | datetime],
    ) -> None:
        mock_agent_uow.agents.get_one_with_face.return_value = returning_agent_data

        agent = await agent_service.get_profile(email="example@email.com")

        mock_agent_uow.agents.get_one_with_face.assert_awaited_once_with(
            {
                "email": "example@email.com",
            }
        )
        assert agent == returning_agent_data

    async def test_get_agent_parameter_with_value(
        self,
        agent_service: AgentService,
        mock_agent_uow: AsyncMock,
        returning_agent_data_with_face: dict[str, str | int | float | datetime],
    ) -> None:
        email = "example@email.com"

        mock_agent_uow.agents.get_one_with_face.return_value = (
            returning_agent_data_with_face
        )

        value = await agent_service.get_agent_parameter(email, "email")

        mock_agent_uow.agents.get_one_with_face.assert_awaited_once_with(
            {
                "email": email,
            }
        )
        assert value == email

    async def test_get_agent_parameter_with_none(
        self,
        agent_service: AgentService,
        mock_agent_uow: AsyncMock,
        returning_agent_data_with_face: dict[str, str | int | float | datetime],
    ) -> None:
        email = "example@email.com"

        mock_agent_uow.agents.get_one_with_face.return_value = (
            returning_agent_data_with_face
        )

        value = await agent_service.get_agent_parameter(email, "no_exists")

        mock_agent_uow.agents.get_one_with_face.assert_awaited_once_with(
            {
                "email": email,
            }
        )
        assert value is None
