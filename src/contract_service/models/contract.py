from datetime import datetime

from sqlalchemy import Enum
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.core.database.base import Base
from src.core.dependencies import (
    int_pk,
    int_not_null,
)

from src.contract_service.schemes.contract import (
    Statuses,
    ContractScheme,
)


class Contract(Base, scheme=ContractScheme):
    __tablename__ = "contracts"

    id: Mapped[int_pk]
    product_id: Mapped[int]
    date_create: Mapped[datetime] = mapped_column(nullable=False)
    date_sign: Mapped[datetime]
    date_begin: Mapped[datetime]
    date_end: Mapped[datetime]
    premium: Mapped[float] = mapped_column(default=0.0)
    insurance_sum: Mapped[float] = mapped_column(default=0.0)
    policy_price: Mapped[float] = mapped_column(default=0.0)
    agent_id: Mapped[int]
    rate: Mapped[float] = mapped_column(default=1.0)
    commission: Mapped[float] = mapped_column(default=0.0)
    status: Mapped[str] = mapped_column(
        Enum(Statuses), default=Statuses.DRAFT, nullable=False
    )
    policy_holder_id: Mapped[int_not_null]
    insured_personal_id: Mapped[int_not_null]
    owner_id: Mapped[int_not_null]
