from typing import AsyncGenerator
import pytest
from fastapi import FastAPI
from httpx import (
    AsyncClient,
    ASGITransport,
)
from asgi_lifespan import LifespanManager
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config import Config
from src.core.database.base import Base
from src.main import App

from tests.data_for_tests import (
    add_ikps,
    add_lobs,
    add_risks,
    add_faces,
    add_agents,
    add_agent_agreements,
)

app: FastAPI = App(config=Config()).initialize()


@pytest.fixture(scope="session")
async def setup_db() -> AsyncGenerator[None, None]:
    config = Config()
    assert config.api.MODE == "TEST", "You try using not 'test.env' file"

    test_engine = create_async_engine(
        url=config.db.URL,
        poolclass=NullPool,
    )
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await add_ikps()
    await add_lobs()
    await add_risks()
    await add_faces()
    await add_agents()
    await add_agent_agreements()

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def client(setup_db: None) -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
            headers={"Content-Type": "application/json"},
        ) as async_test_client:
            yield async_test_client


@pytest.fixture(scope="session", name="pair_tokens")
async def get_auth_user_pair_token(
    client: AsyncClient,
) -> AsyncGenerator[dict[str, str], None]:
    response = await client.post(
        "/auth/register",
        json={
            "email": "example@email.ru",
            "password": "PASSWORD",
        },
    )

    assert response.status_code == 201

    response = await client.post(
        "/auth/login",
        json={
            "email": "example@email.ru",
            "password": "PASSWORD",
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    yield response_data

    await client.post(
        "/auth/logout",
        headers={
            "WWW-Authorization": response_data["access_token"],
        },
    )
