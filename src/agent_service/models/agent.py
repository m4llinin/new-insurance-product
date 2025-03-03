from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.core.database.base import Base
from src.agent_service.schemes.agent import (
    AgentScheme,
    AgentStatuses,
)
from src.core.dependencies import int_pk


class Agent(Base, scheme=AgentScheme):
    __tablename__ = "agents"

    id: Mapped[int_pk]
    email: Mapped[str] = mapped_column(nullable=False)
    face_id: Mapped[int] = mapped_column(ForeignKey("faces.id"), nullable=False)
    ikp_id: Mapped[int] = mapped_column(ForeignKey("ikps.id"), nullable=False)
    status: Mapped[str] = mapped_column(Enum(AgentStatuses), default=AgentStatuses.project.value)
    date_create: Mapped[datetime] = mapped_column(nullable=False)
    date_begin: Mapped[datetime] = mapped_column(nullable=True)
    date_end: Mapped[datetime] = mapped_column(nullable=True)
