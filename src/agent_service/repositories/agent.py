from typing import Any
from loguru import logger
from sqlalchemy import select

from src.agent_service.models import (
    Face,
    Agent,
    Ikp,
    AgentAgreements,
)
from src.core.database.base import SqlAlchemyRepository


class AgentRepository(SqlAlchemyRepository, model=Agent):
    async def get_one_with_face(self, filters: dict[str, Any]) -> dict[str, Any] | None:
        logger.debug(
            "Query for database from {model} with params: {params}",
            model=self._model,
            params=filters,
        )
        stmt = (
            select(
                Agent.id.label("agent_id"),
                Agent,
                Face,
                Ikp.name.label("ikp_name"),
                AgentAgreements,
            )
            .filter_by(**filters)
            .join(Face, Agent.face_id == Face.id)
            .join(Ikp, Agent.ikp_id == Ikp.id)
            .join(AgentAgreements, AgentAgreements.agent_id == Agent.id)
        )
        res = await self._session.execute(stmt)

        res = dict(res.mappings().one())
        for field in ["Agent", "Face", "AgentAgreements"]:
            res.update(res.pop(field).to_dict())

        for field in ["status", "type"]:
            res.update({field: res.get(field).value})

        return res
