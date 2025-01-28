from fastapi import APIRouter, Query
from typing import Annotated

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


@router.get("")
async def get_contracts(
    uow: ContractUOWDep,
    filters: Annotated[ContractFiltersScheme, Query()],
) -> list[ContractScheme]:
    return await ContractService(uow).get_contracts(filters)


@router.post("")
async def add_contract(
    uow: ContractUOWDep,
    contract: ContractAddScheme,
) -> ContractIdResponse:
    contract_id = await ContractService(uow).add_contract(contract)
    return ContractIdResponse(
        id=contract_id,
    )


@router.get("/risks")
async def get_risks(uow: ContractUOWDep) -> list[RiskScheme]:
    return await RiskService(uow).get_risks()


@router.get("/statistics")
async def get_statistics(
    uow: ContractUOWDep,
    agent_id: CurrentUserIdDep,
    period: Annotated[PeriodScheme, Query()],
    broker: BrokerDep,
) -> ContractStatisticsSchemeResponse:
    return await ContractService(uow).get_statistics(
        agent_id=agent_id,
        period=period,
        broker=broker,
    )


@router.post("/price")
async def calculate_police_price(
    uow: ContractUOWDep,
    broker: BrokerDep,
    contract: CalculatePriceScheme,
) -> CalculatePriceResponse:
    return await ContractService(uow).calculate_policy_price(
        contract=contract,
        broker=broker,
    )


@router.post("/premium")
async def calculate_police_premium(
    agent_rate: CurrentUserRateDep,
    contract: CalculatePriceResponse,
) -> CalculatePriceResponse:
    return ContractService.calculate_agent_premium(
        agent_rate=agent_rate,
        contract_price=contract.price,
    )
