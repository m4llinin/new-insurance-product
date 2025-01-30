from typing import Any
from faststream.rabbit.fastapi import RabbitRouter
from loguru import logger
from pydantic import EmailStr

from src.agent_service.api.dependencies import AgentUOWDep
from src.agent_service.services.agent import AgentService

router = RabbitRouter()


@router.subscriber("agent-get-agent")
async def get_agent(
    uow: AgentUOWDep,
    email: EmailStr,
    column: str,
) -> Any | None:
    logger.info(
        "Handling request for 'agent-get-agent' with params: {params}",
        params=[email, column],
    )
    return await AgentService(uow).get_agent_parameter(
        email=email,
        column=column,
    )
