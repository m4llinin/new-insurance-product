from typing import Any

from loguru import logger

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
            logger.debug("Got risks: {risks} from database", risks=risks)
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
            logger.debug(
                "Got risk rates: {rates} for risk_ids: {risk_ids}",
                rates=output_rates,
                risk_ids=risk_ids,
            )
        return output_rates
