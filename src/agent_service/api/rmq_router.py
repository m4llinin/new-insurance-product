from typing import Any
from loguru import logger
from pydantic import EmailStr

from src.agent_service.utils.uow import AgentUOW
from src.core.config import Config
from src.agent_service.services.agent import AgentService
from src.core.rabbit.listener import ListenerRabbit

listener = ListenerRabbit(Config().rmq.URL)


@listener("agent-get-agent", uow=AgentUOW)
async def get_agent(
    email: EmailStr,
    column: str,
    uow: AgentUOW,
) -> Any | None:
    logger.info(
        "Handling request for 'agent-get-agent' with params: {params}",
        params=[email, column],
    )
    return await AgentService(uow).get_agent_parameter(
        email=email,
        column=column,
    )
