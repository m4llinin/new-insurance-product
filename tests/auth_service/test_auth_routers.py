from typing import Any
import pytest
from httpx import AsyncClient


@pytest.mark.usefixtures("client")
class TestAuthRouter:
    user_tokens: dict[str, dict[str, str]] = {}

    async def test_register(
        self,
        client: AsyncClient,
        user_data: list[dict[str, Any]],
    ) -> None:
        for user in user_data:
            response = await client.post(
                "/auth/register",
                json={
                    "email": user.get("email"),
                    "password": user.get("password"),
                },
            )
            response_data = response.json()
            assert response.status_code == 201
            assert "id" in response_data

    async def test_register_duplicate_email(
        self,
        client: AsyncClient,
        user_data: list[dict[str, Any]],
    ) -> None:
        for user in user_data:
            response = await client.post(
                "/auth/register",
                json={
                    "email": user.get("email"),
                    "password": user.get("password"),
                },
            )
            response_data = response.json()
            assert response.status_code == 400
            assert "detail" in response_data
            assert response_data.get("detail") == "User already exists"

    async def test_register_invalid_data(
        self,
        client: AsyncClient,
        invalid_user_data: list[dict[str, Any]],
    ) -> None:
        for user in invalid_user_data:
            response = await client.post(
                "/auth/register",
                json={
                    "email": user.get("email"),
                    "password": user.get("password"),
                },
            )
            response_data = response.json()
            assert response.status_code == 422
            assert "detail" in response_data

    async def test_login(
        self,
        client: AsyncClient,
        user_data: list[dict[str, Any]],
    ) -> None:
        for user in user_data:
            response = await client.post(
                "/auth/login",
                json={
                    "email": user.get("email"),
                    "password": user.get("password"),
                },
            )
            response_data = response.json()
            assert response.status_code == 200
            assert "refresh_token" in response_data
            assert "access_token" in response_data

            self.user_tokens[user.get("email")] = response_data.copy()

    async def test_login_again(
        self,
        client: AsyncClient,
        user_data: list[dict[str, Any]],
    ) -> None:
        for user in user_data:
            response = await client.post(
                "/auth/login",
                json={
                    "email": user.get("email"),
                    "password": user.get("password"),
                },
            )
            response_data = response.json()
            assert response.status_code == 400
            assert "detail" in response_data

    async def test_login_user_not_exists(
        self,
        client: AsyncClient,
        user_not_exists: list[dict[str, Any]],
    ) -> None:
        for user in user_not_exists:
            response = await client.post(
                "/auth/login",
                json={
                    "email": user.get("email"),
                    "password": user.get("password"),
                },
            )
            response_data = response.json()
            assert response.status_code == 400
            assert "detail" in response_data

    async def test_login_invalid_data(
        self,
        client: AsyncClient,
        invalid_user_data: list[dict[str, Any]],
    ) -> None:
        for user in invalid_user_data:
            response = await client.post(
                "/auth/login",
                json={
                    "email": user.get("email"),
                    "password": user.get("password"),
                },
            )
            response_data = response.json()
            assert response.status_code == 422
            assert "detail" in response_data

    async def test_refresh(
        self,
        client: AsyncClient,
        user_data: list[dict[str, Any]],
    ) -> None:
        for user in user_data:
            response = await client.post(
                "/auth/refresh",
                headers={
                    "WWW-Authorization": self.user_tokens[user.get("email")][
                        "refresh_token"
                    ],
                },
            )

            response_data = response.json()
            assert response.status_code == 200
            assert "access_token" in response_data
            assert "refresh_token" in response_data
            assert response_data["refresh_token"] is None

            self.user_tokens[user.get("email")]["access_token"] = response_data[
                "access_token"
            ]

    async def test_refresh_invalid_data(
        self,
        client: AsyncClient,
        invalid_user_tokens,
    ) -> None:
        for token in invalid_user_tokens:
            response = await client.post(
                "/auth/refresh",
                headers={
                    "WWW-Authorization": token,
                },
            )
            response_data = response.json()
            assert response.status_code == 400
            assert "detail" in response_data

    async def test_refresh_with_access_token(
        self,
        client: AsyncClient,
        user_data: list[dict[str, Any]],
    ) -> None:
        for user in user_data:
            response = await client.post(
                "/auth/refresh",
                headers={
                    "WWW-Authorization": self.user_tokens[user.get("email")][
                        "access_token"
                    ],
                },
            )
            response_data = response.json()
            assert response.status_code == 400
            assert "detail" in response_data

    async def test_logout_with_refresh_token(
        self,
        client: AsyncClient,
        user_data: list[dict[str, Any]],
    ) -> None:
        for user in user_data:
            response = await client.post(
                "/auth/logout",
                headers={
                    "WWW-Authorization": self.user_tokens[user.get("email")][
                        "refresh_token"
                    ],
                },
            )
            response_data = response.json()
            assert response.status_code == 400
            assert "detail" in response_data

    async def test_logout(
        self,
        client: AsyncClient,
        user_data: list[dict[str, Any]],
    ) -> None:
        for user in user_data:
            response = await client.post(
                "/auth/logout",
                headers={
                    "WWW-Authorization": self.user_tokens[user.get("email")][
                        "access_token"
                    ],
                },
            )
            response_data = response.json()
            assert response.status_code == 200
            assert "id" in response_data

    async def test_logout_invalid_data(
        self,
        client: AsyncClient,
        invalid_user_tokens: list[Any],
    ) -> None:
        for token in invalid_user_tokens:
            response = await client.post(
                "/auth/logout",
                headers={
                    "WWW-Authorization": token,
                },
            )
            response_data = response.json()
            assert response.status_code == 400
            assert "detail" in response_data

    async def test_logout_without_activate(
        self,
        client: AsyncClient,
        user_data: list[dict[str, Any]],
    ) -> None:
        for user in user_data:
            response = await client.post(
                "/auth/logout",
                headers={
                    "WWW-Authorization": self.user_tokens[user.get("email")][
                        "access_token"
                    ],
                },
            )
            response_data = response.json()
            assert response.status_code == 400
            assert "detail" in response_data
