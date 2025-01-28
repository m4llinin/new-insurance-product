from fastapi import APIRouter

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


@router.get("/")
async def get_agent(
    uow: AgentUOWDep,
    email: CurrentUserDep,
) -> AgentResponse:
    return await AgentService(uow).get_profile(
        email=email,
    )
