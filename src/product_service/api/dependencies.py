from typing import Annotated
from fastapi import (
    Depends,
    HTTPException,
    status,
)

from src.core.dependencies import (
    TokenDep,
    BrokerDep,
)
from src.core.utils.auth import check_auth

from src.product_service.utils.uow import ProductUOW


async def is_auth(
    token: TokenDep,
    broker: BrokerDep,
):
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


ProductUOWDep = Annotated[ProductUOW, Depends(ProductUOW)]
AuthDep = Depends(is_auth)
