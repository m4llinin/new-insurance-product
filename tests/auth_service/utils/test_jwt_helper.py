import pytest
from typing import Any
from src.auth_service.utils.jwt_helper import JWTHelper


@pytest.fixture
def user_payload() -> dict[str, str | int]:
    return {
        "user_id": 1,
        "username": "test_user",
    }


@pytest.fixture
def access_token(jwt_helper: JWTHelper, user_payload: dict[str, str | int]) -> str:
    return jwt_helper.create_token("access", user_payload)


@pytest.fixture
def refresh_token(jwt_helper: JWTHelper, user_payload: dict[str, str | int]) -> str:
    return jwt_helper.create_token("refresh", user_payload)


class TestJWTHelper:
    def test_encode_and_decode_jwt(
        self,
        jwt_helper: JWTHelper,
        user_payload: dict[str, str | int],
    ) -> None:
        token = jwt_helper.encode_jwt(user_payload)
        decoded = jwt_helper.decode_jwt(token)
        assert decoded == user_payload

    def test_create_access_token(
        self,
        jwt_helper: JWTHelper,
        access_token: str,
    ) -> None:
        decoded = jwt_helper.decode_jwt(access_token)
        assert decoded["type"] == "access"
        assert decoded["user_id"] == 1
        assert "exp" in decoded
        assert "iat" in decoded

    def test_create_refresh_token(
        self,
        jwt_helper: JWTHelper,
        refresh_token: str,
    ) -> None:
        decoded = jwt_helper.decode_jwt(refresh_token)
        assert decoded["type"] == "refresh"
        assert decoded["user_id"] == 1
        assert "exp" in decoded
        assert "iat" in decoded

    def test_decode_and_check_valid_token(
        self,
        jwt_helper: JWTHelper,
        access_token: str,
    ) -> None:
        decoded = jwt_helper.decode_and_check_token("access", access_token)
        assert decoded["type"] == "access"

    def test_decode_and_check_invalid_token_type(
        self,
        jwt_helper: JWTHelper,
        access_token: str,
    ) -> None:
        with pytest.raises(ValueError, match="Invalid token"):
            jwt_helper.decode_and_check_token("refresh", access_token)

    def test_decode_invalid_token(self, jwt_helper: JWTHelper) -> None:
        with pytest.raises(ValueError, match="Invalid token"):
            jwt_helper.decode_and_check_token("access", "invalid_token")

    def test_create_pair_tokens(
        self,
        jwt_helper: JWTHelper,
        user_payload: dict[str, Any],
    ) -> None:
        tokens = jwt_helper.create_pair_tokens(user_payload)
        assert "access_token" in tokens
        assert "refresh_token" in tokens

        access_decoded = jwt_helper.decode_jwt(tokens["access_token"])
        refresh_decoded = jwt_helper.decode_jwt(tokens["refresh_token"])
        assert access_decoded["type"] == "access"
        assert refresh_decoded["type"] == "refresh"
