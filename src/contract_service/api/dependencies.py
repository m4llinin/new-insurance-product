from typing import Annotated
from fastapi import (
    HTTPException,
    status,
    Depends,
)

from src.core.dependencies import (
    TokenDep,
    BrokerDep,
)
from src.core.utils.auth import (
    check_auth,
    get_auth_user,
)

from src.contract_service.utils.uow import ContractUOW
from src.contract_service.utils.agent import get_agent


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
            detail="User is unauthorized",
        )
    return response


async def get_current_user_id(
    token: TokenDep,
    broker: BrokerDep,
) -> int:
    response = await get_auth_user(
        token=token,
        broker=broker,
    )
    if not response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized",
        )

    response = await get_agent(
        email=response,
        broker=broker,
        column="agent_id",
    )
    if not response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )

    return response


async def get_current_user_rate(
    token: TokenDep,
    broker: BrokerDep,
) -> float:
    response = await get_auth_user(
        token=token,
        broker=broker,
    )
    if not response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized",
        )

    response = await get_agent(
        email=response,
        broker=broker,
        column="rate",
    )
    if not response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )

    return response


ContractUOWDep = Annotated[ContractUOW, Depends(ContractUOW)]
AuthDep = Depends(is_auth)
CurrentUserIdDep = Annotated[int, Depends(get_current_user_id)]
CurrentUserRateDep = Annotated[int, Depends(get_current_user_rate)]
