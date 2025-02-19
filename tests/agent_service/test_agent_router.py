from typing import Any
import pytest
from httpx import AsyncClient


@pytest.mark.usefixtures("client")
class TestAgentRouter:
    async def test_agent(
        self,
        client: AsyncClient,
        pair_tokens: dict[str, Any],
    ) -> None:
        response = await client.get(
            "/agent",
            headers={
                "WWW-Authorization": pair_tokens["access_token"],
            },
        )

        print(response.json())
        assert response.status_code == 200
        assert response.json() == {}