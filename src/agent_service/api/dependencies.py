from fastapi import (
    Depends,
    HTTPException,
    status,
)
from typing import Annotated
from pydantic import EmailStr

from src.agent_service.utils.uow import AgentUOW
from src.core.dependencies import (
    TokenDep,
    BrokerDep,
)
from src.core.utils.auth import (
    check_auth,
    get_auth_user,
)


async def is_auth(
    token: TokenDep,
    broker: BrokerDep,
) -> bool:
    response = await check_auth(
        token=token,
        broker=broker,
    )
    if not response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return response


async def get_current_user(
    token: TokenDep,
    broker: BrokerDep,
) -> EmailStr:
    response = await get_auth_user(
        token=token,
        broker=broker,
    )
    if not response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    return response


AgentUOWDep = Annotated[AgentUOW, Depends(AgentUOW)]
AuthDep = Depends(is_auth)
CurrentUserDep = Annotated[EmailStr, Depends(get_current_user)]
