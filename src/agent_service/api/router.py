from fastapi import APIRouter
from loguru import logger

from src.agent_service.api.dependencies import (
    AgentUOWDep,
    AuthDep,
    CurrentUserDep,
)
from src.agent_service.services.agent import AgentService
from src.agent_service.schemes.agent import AgentResponse

router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
    dependencies=[AuthDep],
)


@router.get("", response_model=AgentResponse)
async def get_agent(
    uow: AgentUOWDep,
    email: CurrentUserDep,
):
    logger.info("Handling request for GET '/agent' with params: {params}", params=email)
    return await AgentService(uow).get_profile(
        email=email,
    )
