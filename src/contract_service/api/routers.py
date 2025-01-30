from fastapi import APIRouter, Query
from typing import Annotated
from loguru import logger

from src.contract_service.api.dependencies import (
    AuthDep,
    ContractUOWDep,
    CurrentUserIdDep,
    CurrentUserRateDep,
)
from src.contract_service.schemes.risk import RiskScheme
from src.contract_service.schemes.contract import (
    ContractScheme,
    ContractFiltersScheme,
    ContractAddScheme,
    ContractIdResponse,
    PeriodScheme,
    ContractStatisticsSchemeResponse,
    CalculatePriceScheme,
    CalculatePriceResponse,
)
from src.contract_service.services.risk import RiskService
from src.contract_service.services.contract import ContractService
from src.core.dependencies import BrokerDep

router = APIRouter(
    prefix="/contracts",
    tags=["Contracts"],
    dependencies=[AuthDep],
)


@router.get("", response_model=list[ContractScheme])
async def get_contracts(
    uow: ContractUOWDep,
    filters: Annotated[ContractFiltersScheme, Query()],
):
    logger.info(
        "Handling request for GET '/contracts' with params: {params}",
        params=filters,
    )
    return await ContractService(uow).get_contracts(filters)


@router.post("", response_model=ContractIdResponse)
async def add_contract(
    uow: ContractUOWDep,
    contract: ContractAddScheme,
):
    logger.info(
        "Handling request for POST '/contracts' with params: {params}",
        params=contract,
    )
    contract_id = await ContractService(uow).add_contract(contract)
    return ContractIdResponse(
        id=contract_id,
    )


@router.get("/risks", response_model=list[RiskScheme])
async def get_risks(uow: ContractUOWDep):
    logger.info("Handling request for GET '/contracts/risks'")
    return await RiskService(uow).get_risks()


@router.get("/statistics", response_model=ContractStatisticsSchemeResponse)
async def get_statistics(
    uow: ContractUOWDep,
    agent_id: CurrentUserIdDep,
    period: Annotated[PeriodScheme, Query()],
    broker: BrokerDep,
):
    logger.info(
        "Handling request for GET '/contracts/statistics' with params: {params}",
        params=[agent_id,period],
    )
    return await ContractService(uow).get_statistics(
        agent_id=agent_id,
        period=period,
        broker=broker,
    )


@router.post("/price", response_model=CalculatePriceResponse)
async def calculate_police_price(
    uow: ContractUOWDep,
    broker: BrokerDep,
    contract: CalculatePriceScheme,
):
    logger.info(
        "Handling request for POST '/contracts/price' with params: {params}",
        params=contract,
    )
    return await ContractService(uow).calculate_policy_price(
        contract=contract,
        broker=broker,
    )


@router.post("/premium", response_model=CalculatePriceResponse)
async def calculate_police_premium(
    agent_rate: CurrentUserRateDep,
    contract: CalculatePriceResponse,
):
    logger.info(
        "Handling request for POST '/contracts/premium' with params: {params}",
        params=contract,
    )
    return await ContractService().calculate_agent_premium(
        agent_rate=agent_rate,
        contract_price=contract.price,
    )
