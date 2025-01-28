from typing import Any

from src.contract_service.utils.uow import ContractUOW


class ContractRiskService:
    def __init__(self, uow: ContractUOW):
        self._uow = uow

    async def add_contract_risk(self, data: dict[str, Any]) -> int:
        async with self._uow:
            contract_risk_id = await self._uow.contract_risks.insert(data)
            await self._uow.commit()
            return contract_risk_id

    async def get_contract_risk(self, contract_id: int) -> list[int]:
        async with self._uow:
            contract_risk = await self._uow.contract_risks.get_one(
                {
                    "contract_id": contract_id,
                }
            )

            if contract_risk is None:
                raise ValueError(
                    f"Contract risk not found: {contract_id}",
                )

            return contract_risk.risk_id
