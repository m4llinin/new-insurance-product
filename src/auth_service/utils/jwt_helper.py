from datetime import (
    datetime,
    UTC,
    timedelta,
)
from jwt import (
    PyJWT,
    PyJWTError,
)
from typing import (
    Literal,
    Any,
)

from src.core.config import Config


class JWTHelper:
    def __init__(self) -> None:
        self.__jwt = PyJWT()
        self._config = Config()

    def encode_jwt(self, payload: dict[str, Any]) -> str:
        return self.__jwt.encode(
            payload=payload,
            key=self._config.auth.SECRET_KEY,
            algorithm=self._config.auth.ALGORITHM,
        )

    def decode_jwt(self, token: str) -> Any:
        return self.__jwt.decode(
            jwt=token,
            key=self._config.auth.SECRET_KEY,
            algorithms=[
                self._config.auth.ALGORITHM,
            ],
        )

    def create_token(
        self,
        token_type: Literal["access", "refresh"],
        payload: dict[str, Any],
    ) -> str:
        to_encode = payload.copy()
        now = datetime.now(tz=UTC)

        if token_type == "access":
            expires = now + timedelta(
                minutes=self._config.auth.ACCESS_TOKEN_EXPIRE_MINUTES,
            )
        else:
            expires = now + timedelta(
                days=self._config.auth.REFRESH_TOKEN_EXPIRE_DAYS,
            )

        to_encode.update(
            {
                "type": token_type,
                "exp": expires,
                "iat": now,
            }
        )

        return self.encode_jwt(to_encode)

    def decode_and_check_token(
        self,
        type_token: Literal["access", "refresh"],
        token: str,
    ) -> Any:
        try:
            decoded_token = self.decode_jwt(token)
        except PyJWTError:
            raise ValueError("Invalid token")

        type_token_from_dict = decoded_token.get("type")
        if type_token_from_dict != type_token:
            raise ValueError("Invalid token")

        return decoded_token

    def create_pair_tokens(self, user_payload: dict[str, Any]) -> dict[str, str]:
        access_token = self.create_token(
            token_type="access",
            payload=user_payload,
        )
        refresh_token = self.create_token(
            token_type="refresh",
            payload=user_payload,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
