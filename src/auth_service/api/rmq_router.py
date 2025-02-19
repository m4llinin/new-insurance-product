from faststream.rabbit.fastapi import RabbitRouter
from loguru import logger
from pydantic import EmailStr

from src.core.config import Config

from src.auth_service.services.auth import AuthService
from src.auth_service.api.dependencies import AuthUOWDep


router = RabbitRouter(Config().rmq.URL)


@router.subscriber("auth-check")
async def check_auth(uow: AuthUOWDep, token: str) -> bool:
    logger.info("Handling request for 'auth-check' with params: {params}", params=token)
    response = False

    try:
        response = await AuthService(uow).check_user_is_authorized(token)
    except ValueError:
        pass

    return response


@router.subscriber("auth-get-user")
async def get_user(uow: AuthUOWDep, token: str) -> EmailStr:
    logger.info(
        "Handling request for 'auth-get-user' with params: {params}", params=token
    )
    return await AuthService(uow).get_current_user(token)
