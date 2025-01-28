from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import ForeignKey

from src.core.database.base import Base
from src.core.dependencies import (
    int_pk,
    int_not_null,
)
from src.agent_service.schemes.agent_agreements import AgentAgreementsScheme


class AgentAgreements(Base, scheme=AgentAgreementsScheme):
    __tablename__ = "agent_agreements"

    id: Mapped[int_pk]
    agent_id: Mapped[int] = mapped_column(ForeignKey("agents.id"), nullable=False)
    lob_id: Mapped[int_not_null]
    rate: Mapped[float] = mapped_column(nullable=False)
