from typing import Any
from loguru import logger

from src.agent_service.utils.uow import AgentUOW
from src.core.utils.base_service import BaseService
from src.core.cache.helper import CacheHelper


class AgentService(BaseService):
    def __init__(self, uow: AgentUOW):
        self._uow = uow

    async def add(self, agent: dict[str, Any]) -> int:
        async with self._uow:
            agent_id = await self._uow.agents.insert(agent)
            await self._uow.commit()
            return agent_id

    @CacheHelper.cache()
    async def get_profile(self, email: str) -> dict[str, Any]:
        async with self._uow:
            agent = await self._uow.agents.get_one_with_face(
                {
                    "email": email,
                }
            )
            logger.debug("Got from database rows: {res}", res=agent)
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
            logger.debug("Got from database rows: {res}", res=agent)
        return agent.get(column)
