from typing import Any
from sqlalchemy import select

from src.contract_service.models import ContractRisk
from src.core.database.base import SqlAlchemyRepository
from src.contract_service.models.contract import Contract
from src.contract_service.schemes.contract import ContractScheme


class ContractRepository(SqlAlchemyRepository, model=Contract):
    async def get_all(self, filters: dict[str, Any]) -> list[Any]:
        date_begin = filters.pop("date_begin", None)
        date_end = filters.pop("date_end", None)

        stmt = (
            select(Contract, ContractRisk.risk_id)
            .filter_by(**filters)
            .join(ContractRisk, Contract.id == ContractRisk.contract_id)
        )
        if date_begin is not None and date_end is not None:
            stmt = stmt.filter(
                date_begin <= Contract.date_sign,
                date_end >= Contract.date_sign,
            )

        res = await self._session.execute(stmt)
        out = []
        for row in res.mappings():
            row_dict = dict(row)
            row_dict.update(row_dict.pop("Contract").to_dict())
            out.append(ContractScheme(**row_dict))
        return out
