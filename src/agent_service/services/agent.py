from typing import Any

from src.agent_service.utils.uow import AgentUOW
from src.agent_service.schemes.agent import AgentResponse


class AgentService:
    def __init__(self, uow: AgentUOW):
        self._uow = uow

    async def get_profile(self, email: str) -> AgentResponse:
        async with self._uow:
            agent = await self._uow.agents.get_one_with_face(
                {
                    "email": email,
                }
            )
        return agent

    async def get_agent_parameter(
        self,
        email: str,
        column: str,
    ) -> Any | None:
        async with self._uow:
            agent = await self._uow.agents.get_one_with_face(
                {
                    "email": email,
                }
            )
        return agent.get(column)
