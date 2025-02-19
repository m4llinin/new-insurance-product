from typing import Any

from src.core.utils.base_service import BaseService
from src.agent_service.utils.uow import AgentUOW


class FaceService(BaseService):
    def __init__(self, uow: AgentUOW) -> None:
        self._uow = uow

    async def add(self, face: dict[str, Any]) -> int:
        async with self._uow:
            face_id = await self._uow.faces.insert(face)
            await self._uow.commit()
            return face_id
