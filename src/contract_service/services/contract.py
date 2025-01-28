from typing import Any
from faststream.rabbit.fastapi import RabbitBroker

from src.contract_service.utils.uow import ContractUOW
from src.contract_service.schemes.contract import (
    ContractAddScheme,
    ContractFiltersScheme,
    ContractScheme,
    ContractStatisticsSchemeResponse,
    PeriodScheme,
    ProductStatisticsScheme,
    ProductCommissionPremium,
    OneContractSchemeResponse,
    ProductScheme,
    CalculatePriceScheme,
    CalculatePriceResponse,
)
from src.contract_service.services.contract_risks import ContractRiskService
from src.contract_service.services.risk import RiskService


class ContractService:
    def __init__(self, uow: ContractUOW) -> None:
        self._uow = uow

    @staticmethod
    async def get_products_without_metafields(
        product_ids: list[int],
        broker: RabbitBroker,
    ) -> list[ProductStatisticsScheme]:
        response = await broker.request(
            message=product_ids,
            routing_key="prod-get-products-without-metafields",
        )

        return [ProductStatisticsScheme(**r) for r in await response.decode()]

    @staticmethod
    async def get_rates_products_and_metafields(
        product: dict[str, Any],
        broker: RabbitBroker,
    ) -> dict[str, Any]:
        response = await broker.request(
            message=product,
            routing_key="prod-get-rates-products-and-metafields",
        )
        return await response.decode()

    async def get_contracts(
        self, filters: ContractFiltersScheme
    ) -> list[ContractScheme]:
        filters_dict = filters.model_dump(exclude_none=True)
        async with self._uow:
            contracts = await self._uow.contracts.get_all(filters_dict)
            return contracts

    async def add_contract(self, contract: ContractAddScheme) -> int:
        contract_dict = contract.model_dump()
        risks = contract_dict.pop("risk_id")

        async with self._uow:
            contract_id = await self._uow.contracts.insert(contract_dict)
            await self._uow.commit()

        await ContractRiskService(self._uow).add_contract_risk(
            {
                "contract_id": contract_id,
                "risk_id": risks,
                "premium": contract_dict.get("premium"),
                "insurance_sum": contract_dict.get("insurance_sum"),
            }
        )

        return contract_id

    async def get_statistics(
        self,
        agent_id: int,
        period: PeriodScheme,
        broker: RabbitBroker,
    ) -> ContractStatisticsSchemeResponse:
        period_dict = period.model_dump()
        period_dict.update(
            {
                "agent_id": agent_id,
            }
        )

        all_contract_commission = 0
        all_contract_premium = 0
        product_ids = set()
        async with self._uow:
            contracts = await self._uow.contracts.get_all(period_dict)

        products_statistics = {}
        for contract in contracts:
            all_contract_commission += contract.commission
            all_contract_premium += contract.premium
            product_ids.add(contract.product_id)

            product_stats = products_statistics.setdefault(
                str(contract.product_id), ProductCommissionPremium()
            )
            product_stats.premium += contract.premium
            product_stats.commission += contract.commission
            products_statistics[str(contract.product_id)] = product_stats

        product_ids = list(product_ids)
        products = await self.get_products_without_metafields(
            product_ids=product_ids,
            broker=broker,
        )

        for product in products:
            product_stats = products_statistics.get(str(product.id))
            product.all_premium = product_stats.premium
            product.all_commission = product_stats.commission
            products_statistics[str(product.id)] = product

        output_contracts = []
        for contract in contracts:
            product_dict = products_statistics.get(
                str(contract.product_id)
            ).model_dump()
            contract_dict = contract.model_dump()
            output_contracts.append(
                OneContractSchemeResponse(
                    product=ProductScheme(**product_dict),
                    **contract_dict,
                )
            )

        return ContractStatisticsSchemeResponse(
            contracts=output_contracts,
            all_premium=all_contract_premium,
            all_commission=all_contract_commission,
            products=products,
        )

    async def calculate_policy_price(
        self,
        contract: CalculatePriceScheme,
        broker: RabbitBroker,
    ) -> CalculatePriceResponse:
        product_meta_fields_rates = await self.get_rates_products_and_metafields(
            product={
                "product_id": contract.product_id,
                "meta_fields": contract.meta_fields,
            },
            broker=broker,
        )
        product_rate = product_meta_fields_rates.get("product_rate")
        meta_field_rates = product_meta_fields_rates.get("meta_fields")
        risk_rates = await RiskService(self._uow).get_rates(contract.risk_id)

        price = (contract.insurance_sum / product_rate) * 0.0003
        price *= contract.count_days
        price *= product_rate

        for rate in risk_rates:
            price *= rate

        for rate in meta_field_rates:
            price *= rate

        return CalculatePriceResponse(
            price=price,
        )

    @staticmethod
    def calculate_agent_premium(
        agent_rate: float,
        contract_price: float,
    ) -> CalculatePriceResponse:
        return CalculatePriceResponse(
            price=contract_price * (agent_rate / 100),
        )
