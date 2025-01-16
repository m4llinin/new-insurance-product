from faststream.rabbit.fastapi import RabbitRouter

from src.core.config import Config

from src.auth_service.schemas.auth import AuthScheme
from src.auth_service.services.auth import AuthService
from src.auth_service.api.dependencies import AuthUOWDep


router = RabbitRouter(Config().rmq.url())


@router.subscriber("auth-check")
async def check_auth(uow: AuthUOWDep, token: str) -> bool:
    response = False

    try:
        response = await AuthService(uow).check_user_is_authorized(token)
    except ValueError:
        pass

    return response


@router.subscriber("auth-get-user")
async def get_user(uow: AuthUOWDep, token: str) -> AuthScheme:
    return await AuthService(uow).get_current_user(token)
