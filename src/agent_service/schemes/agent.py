from datetime import datetime
from typing import Type
from pydantic import (
    BaseModel,
    field_serializer,
)
from enum import Enum

from src.agent_service.schemes.face import TypeFace


class AgentStatuses(Enum):
    project = "project"
    active = "active"
    ended = "ended"
    terminated = "terminated"


class AgentScheme(BaseModel):
    id: int
    email: str
    face_id: int
    ikp_id: int
    status: AgentStatuses
    date_create: datetime
    date_begin: datetime | None = None
    date_end: datetime | None = None

    @field_serializer("status")
    def serialize_status(self, status: Type[Enum], _info):
        return status.value


class AgentResponse(BaseModel):
    type: TypeFace
    first_name: str | None = None
    second_name: str | None = None
    last_name: str | None = None
    date_of_birth: datetime | None = None
    name: str | None = None
    inn: int
    ikp_name: str
    status: AgentStatuses
    date_begin: datetime | None = None
    date_end: datetime | None = None
