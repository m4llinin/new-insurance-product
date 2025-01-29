from typing import Any

from src.agent_service.utils.uow import AgentUOW
from src.core.utils.base_service import BaseService
from src.core.cache.helper import CacheHelper


class AgentService(BaseService):
    def __init__(self, uow: AgentUOW):
        self._uow = uow

    @CacheHelper.cache()
    async def get_profile(self, email: str) -> dict[str, Any]:
        async with self._uow:
            agent = await self._uow.agents.get_one_with_face(
                {
                    "email": email,
                }
            )
        return agent

    @CacheHelper.cache()
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
