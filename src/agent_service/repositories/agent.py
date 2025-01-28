from typing import Any

from sqlalchemy import select

from src.agent_service.models import (
    Face,
    Agent,
    Ikp,
)
from src.core.database.base import SqlAlchemyRepository


class AgentRepository(SqlAlchemyRepository, model=Agent):
    async def get_one_with_face(self, filters: dict[str, Any]) -> dict[str, Any]:
        stmt = (
            select(Agent.id.label("agent_id"), Agent, Face, Ikp.name.label("ikp_name"))
            .filter_by(**filters)
            .join(Face, Agent.face_id == Face.id)
            .join(Ikp, Agent.ikp_id == Ikp.id)
        )
        res = await self._session.execute(stmt)

        res = dict(next(res.mappings()))
        for field in ["Agent", "Face"]:
            res.update(res.pop(field).to_dict())
        return res
