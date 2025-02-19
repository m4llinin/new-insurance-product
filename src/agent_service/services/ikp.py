from typing import Any

from src.core.utils.base_service import BaseService
from src.agent_service.utils.uow import AgentUOW


class IkpService(BaseService):
    def __init__(self, uow: AgentUOW) -> None:
        self._uow = uow

    async def add(self, ikp: dict[str, Any]) -> int:
        async with self._uow:
            ikp_id = await self._uow.ikps.insert(ikp)
            await self._uow.commit()
            return ikp_id
