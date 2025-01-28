from sqlalchemy import ForeignKey, ARRAY, Integer
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.core.database.base import Base
from src.core.dependencies import int_pk

from src.contract_service.schemes.contract_risks import ContractRiskScheme


class ContractRisk(Base, scheme=ContractRiskScheme):
    __tablename__ = "contract_risks"
    id: Mapped[int_pk]
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"), nullable=False)
    risk_id: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    premium: Mapped[float] = mapped_column(default=0.0)
    insurance_sum: Mapped[float] = mapped_column(default=0.0)
