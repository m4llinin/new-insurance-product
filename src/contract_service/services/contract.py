from typing import Any
from loguru import logger

from src.contract_service.utils.uow import ContractUOW
from src.contract_service.schemes.contract import (
    ContractAddScheme,
    ContractFiltersScheme,
    PeriodScheme,
    ProductStatisticsScheme,
    ProductCommissionPremium,
    OneContractSchemeResponse,
    CalculatePriceScheme,
)
from src.contract_service.services.contract_risks import ContractRiskService
from src.contract_service.services.risk import RiskService
from src.core.rabbit.broker import BrokerRabbit
from src.core.utils.base_service import BaseService
from src.core.cache.helper import CacheHelper


class ContractService(BaseService):
    def __init__(self, uow: ContractUOW = None) -> None:
        self._uow = uow

    @staticmethod
    async def get_products_without_metafields(
        product_ids: list[int],
        broker: BrokerRabbit,
    ) -> list[ProductStatisticsScheme]:
        response = await broker.request(
            message={
                "product_ids": product_ids,
            },
            routing_key="prod-get-products-without-metafields",
        )
        return [ProductStatisticsScheme(**r) for r in response]

    @staticmethod
    async def get_rates_products_and_metafields(
        product: dict[str, Any],
        broker: BrokerRabbit,
    ) -> dict[str, Any]:
        response = await broker.request(
            message=product,
            routing_key="prod-get-rates-products-and-metafields",
        )
        return response

    @CacheHelper.cache()
    async def get_contracts(
        self, filters: ContractFiltersScheme
    ) -> list[dict[str, Any]]:
        filters_dict = filters.model_dump(exclude_none=True)
        async with self._uow:
            contracts = await self._uow.contracts.get_all(filters_dict)
        logger.debug(
            "Got contracts: {contracts} with params: {params}",
            contracts=contracts,
            params=filters,
        )
        return [contract.model_dump() for contract in contracts]

    async def add_contract(self, contract: ContractAddScheme) -> int:
        contract_dict = contract.model_dump()
        risks = contract_dict.pop("risk_id")

        async with self._uow:
            contract_id = await self._uow.contracts.insert(contract_dict)
            await self._uow.commit()
        logger.debug(
            "Contract: {contract} was insert with id: {id}",
            contract=contract,
            id=contract_id,
        )

        await ContractRiskService(self._uow).add_contract_risk(
            {
                "contract_id": contract_id,
                "risk_id": risks,
                "premium": contract_dict.get("premium"),
                "insurance_sum": contract_dict.get("insurance_sum"),
            }
        )

        return contract_id

    @CacheHelper.cache()
    async def get_statistics(
        self,
        agent_id: int,
        period: PeriodScheme,
        broker: BrokerRabbit,
    ) -> dict[str, Any]:
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
        logger.debug(
            "Got contracts: {contracts} with params: {params}",
            contracts=contracts,
            params=[agent_id, period],
        )

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
        logger.debug(
            "Got products: {products} with params: {params}",
            products=products,
            params=product_ids,
        )

        for product in products:
            product_stats = products_statistics.get(str(product.id))
            product.all_premium = product_stats.premium
            product.all_commission = product_stats.commission
            products_statistics[str(product.id)] = product.model_dump()

        output_contracts = []
        for contract in contracts:
            product_dict = products_statistics.get(str(contract.product_id))
            contract_dict = contract.model_dump()
            output_contracts.append(
                OneContractSchemeResponse(
                    product=product_dict,
                    **contract_dict,
                ).model_dump()
            )

        return {
            "contracts": output_contracts,
            "all_premium": all_contract_premium,
            "all_commission": all_contract_commission,
            "products": [product.model_dump() for product in products],
        }

    @CacheHelper.cache()
    async def calculate_policy_price(
        self,
        contract: CalculatePriceScheme,
        broker: BrokerRabbit,
    ) -> dict[str, Any]:
        product_meta_fields_rates = await self.get_rates_products_and_metafields(
            product={
                "product_id": contract.product_id,
                "meta_fields": [mt.model_dump() for mt in contract.meta_fields],
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

        logger.debug(
            "Calculate contract price:{price} with params: {contract}",
            price=price,
            contract=contract,
        )
        return {
            "price": price,
        }

    @CacheHelper.cache()
    async def calculate_agent_premium(
        self,
        agent_rate: float,
        contract_price: float,
    ) -> dict[str, Any]:
        return {
            "price": contract_price * (agent_rate / 100),
        }
