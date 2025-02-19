from typing import Any

from src.core.utils.base_service import BaseService
from src.agent_service.utils.uow import AgentUOW


class AgentAgreementsService(BaseService):
    def __init__(self, uow: AgentUOW) -> None:
        self._uow = uow

    async def add(self, agent_agreement: dict[str, Any]) -> int:
        async with self._uow:
            agent_agreement_id = await self._uow.agent_agreements.insert(
                agent_agreement
            )
            await self._uow.commit()
            return agent_agreement_id
