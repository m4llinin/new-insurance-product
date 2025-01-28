from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base
from src.core.dependencies import (
    int_pk,
    str_not_null,
)

from src.contract_service.schemes.risk import RiskScheme


class Risk(Base, scheme=RiskScheme):
    __tablename__ = "risks"
    id: Mapped[int_pk]
    name: Mapped[str_not_null]
    rate: Mapped[float] = mapped_column(default=1.0, nullable=False)
