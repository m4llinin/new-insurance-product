from loguru import logger
from pydantic import EmailStr

from src.auth_service.utils.uow import AuthUOW
from src.core.config import Config
from src.auth_service.services.auth import AuthService
from src.core.rabbit.listener import ListenerRabbit

listener = ListenerRabbit(Config().rmq.URL)


@listener("auth-check", uow=AuthUOW)
async def check_auth(token: str, uow: AuthUOW) -> bool:
    logger.info("Handling request for 'auth-check' with params: {params}", params=token)
    response = False

    try:
        response = await AuthService(uow).check_user_is_authorized(token)
    except ValueError:
        pass

    return response


@listener("auth-get-user", uow=AuthUOW)
async def get_user(token: str, uow: AuthUOW) -> EmailStr:
    logger.info(
        "Handling request for 'auth-get-user' with params: {params}", params=token
    )
    return await AuthService(uow).get_current_user(token)
