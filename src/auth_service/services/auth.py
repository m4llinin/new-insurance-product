from typing import Any
from pydantic import EmailStr
from loguru import logger

from src.auth_service.utils.uow import AuthUOW
from src.auth_service.utils.jwt_helper import JWTHelper
from src.auth_service.utils.pwd_helper import PWDHelper

from src.auth_service.schemes.auth import AuthSchemeRequest
from src.auth_service.exceptions import NotAuthorizedException
from src.core.cache.helper import CacheHelper
from src.core.utils.base_service import BaseService


class AuthService(BaseService):

    def __init__(self, uow: AuthUOW):
        self._uow = uow
        self._pwd_helper = PWDHelper()
        self._jwt_helper = JWTHelper()

    async def register_user(self, credentials: AuthSchemeRequest) -> dict[str, Any]:
        async with self._uow:
            if (
                await self._uow.users.get_one(
                    {
                        "email": credentials.email,
                    }
                )
            ) is not None:
                logger.debug("User: {email} already exists", email=credentials.email)
                raise ValueError("User already exists")

            hashed_password = self._pwd_helper.hash_password(credentials.password)
            user_id = await self._uow.users.insert(
                {
                    "email": credentials.email,
                    "hashed_password": hashed_password,
                }
            )
            logger.debug(
                "User: {email} was insert with id: {id}",
                email=credentials.email,
                id=user_id,
            )
            await self._uow.commit()

        return {
            "id": user_id,
        }

    async def login_user(self, credentials: AuthSchemeRequest) -> dict[str, str]:
        async with self._uow:
            if (
                user := await self._uow.users.get_one(
                    {
                        "email": credentials.email,
                    }
                )
            ) is None:
                logger.debug(
                    "User: {email} enter invalid password or email",
                    email=credentials.email,
                )
                raise ValueError("Invalid password or email")

            if not self._pwd_helper.verify_password(
                password=credentials.password,
                hashed_password=user.hashed_password,
            ):
                logger.debug(
                    "User: {email} enter invalid password or email",
                    email=credentials.email,
                )
                raise ValueError("Invalid password or email")

            if user.is_active:
                logger.debug("User: {email} is already active", email=credentials.email)
                raise ValueError("User is already active")

            await self._uow.users.update(
                filters={
                    "id": user.id,
                },
                data={
                    "is_active": True,
                },
            )
            logger.debug("User: {email} was activated", email=credentials.email)
            await self._uow.commit()

        pair_tokens = self._jwt_helper.create_pair_tokens(
            {
                "user_id": user.id,
                "sub": user.email,
            }
        )
        logger.debug("Created a pair tokens for user: {email}", email=credentials.email)
        return pair_tokens

    async def logout_user(self, token: str) -> dict[str, Any]:
        decoded_token = self._jwt_helper.decode_and_check_token("access", token)

        async with self._uow:
            user_id = decoded_token.get("user_id")
            await self._uow.users.update(
                filters={
                    "id": user_id,
                },
                data={
                    "is_active": False,
                },
            )
            logger.debug("User: {user_id} was deactivated", user_id=user_id)
            await self._uow.commit()

        return {
            "id": user_id,
        }

    async def refresh_token(self, token: str) -> dict[str, Any]:
        decoded_token = self._jwt_helper.decode_and_check_token("refresh", token)

        async with self._uow:
            user_id = decoded_token.get("user_id")
            user = await self._uow.users.get_one(
                {
                    "id": user_id,
                }
            )
        logger.debug("Got user: {user_id} from database", user_id=user_id)

        if user is None:
            logger.debug("User: {user_id} gave invalid token", user_id=user_id)
            raise ValueError("Invalid token")

        if not user.is_active:
            logger.debug("User: {user_id} was not authorized", user_id=user_id)
            raise NotAuthorizedException("User is not authorized")

        access_token = self._jwt_helper.create_token(
            token_type="access",
            payload={
                "user_id": user.id,
                "sub": user.email,
            },
        )
        logger.debug("Created an access token for user: {user_id}", user_id=user_id)
        return {
            "access_token": access_token,
        }

    @CacheHelper.cache()
    async def get_current_user(self, token: str) -> EmailStr:
        decoded_token = self._jwt_helper.decode_and_check_token("access", token)

        async with self._uow:
            user_id = decoded_token.get("user_id")
            user = await self._uow.users.get_one(
                {
                    "id": user_id,
                }
            )
        logger.debug("Got user: {user_id} from database", user_id=user_id)

        if user is None:
            logger.debug("User: {user_id} gave invalid token", user_id=user_id)
            raise ValueError("Invalid token")

        if not user.is_active:
            logger.debug("User: {user_id} was not authorized", user_id=user_id)
            raise NotAuthorizedException("User is not authorized")

        return user.email

    @CacheHelper.cache()
    async def check_user_is_authorized(self, token: str) -> bool:
        decoded_token = self._jwt_helper.decode_and_check_token("access", token)

        async with self._uow:
            user_id = decoded_token.get("user_id")
            user = await self._uow.users.get_one(
                {
                    "id": user_id,
                }
            )
        logger.debug("Got user: {user_id} from database", user_id=user_id)

        if user is None:
            logger.debug("User: {user_id} gave invalid token", user_id=user_id)
            raise ValueError("Invalid token")

        return user.is_active
