from src.contract_service.utils.uow import ContractUOW


class RiskService:
    def __init__(self, uow: ContractUOW):
        self._uow = uow

    async def get_risks(self):
        async with self._uow:
            return await self._uow.risks.get_all({})

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
