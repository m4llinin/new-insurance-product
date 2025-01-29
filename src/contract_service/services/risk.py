from typing import Any

from src.contract_service.utils.uow import ContractUOW
from src.core.utils.base_service import BaseService
from src.core.cache.helper import CacheHelper


class RiskService(BaseService):
    def __init__(self, uow: ContractUOW):
        self._uow = uow

    @CacheHelper.cache()
    async def get_risks(self) -> list[dict[str, Any]]:
        async with self._uow:
            risks = await self._uow.risks.get_all({})
            return [risk.model_dump() for risk in risks]

    @CacheHelper.cache()
    async def get_rates(self, risk_ids: list[int]) -> list[float]:
        output_rates = []
        async with self._uow:
            for risk_id in risk_ids:
                risk = await self._uow.risks.get_one(
                    {
                        "id": risk_id,
                    }
                )
                output_rates.append(risk.rate)
        return output_rates
