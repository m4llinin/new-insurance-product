from datetime import datetime

import pytest
from unittest.mock import AsyncMock

from src.agent_service.services.agent import AgentService
from src.agent_service.utils.uow import AgentUOW


@pytest.fixture
async def agent_uow() -> AgentUOW:
    return AgentUOW()


@pytest.fixture
async def mock_agent_uow() -> AsyncMock:
    uow = AsyncMock(spec=AgentUOW)
    uow.agents = AsyncMock()
    uow.agent_agreements = AsyncMock()
    uow.ikps = AsyncMock()
    uow.faces = AsyncMock()
    return uow


@pytest.fixture
async def agent_service(mock_agent_uow: AsyncMock) -> AgentService:
    return AgentService(uow=mock_agent_uow)


@pytest.fixture
def agent_data() -> dict[str, str | int | datetime]:
    return {
        "email": "example@email.com",
        "face_id": 1,
        "ikp_id": 1,
        "status": "active",
        "date_create": datetime(2024, 1, 2, 23),
        "date_begin": datetime(2024, 1, 2, 23),
        "date_end": datetime(2024, 1, 3, 20),
    }


@pytest.fixture
def returning_agent_data() -> dict[str, str | int | datetime]:
    return {
        "id": 1,
        "email": "example@email.com",
        "face_id": 1,
        "ikp_id": 1,
        "status": "active",
        "date_create": datetime(2024, 1, 2, 23),
        "date_begin": datetime(2024, 1, 2, 23),
        "date_end": datetime(2024, 1, 3, 20),
    }


@pytest.fixture
def returning_agent_data_with_face() -> dict[str, str | int | float | datetime]:
    return {
        "agent_id": 1,
        "ikp_name": "IKP_NAME",
        "status": "active",
        "type": "legal",
        "id": 1,
        "email": "example@email.com",
        "face_id": 1,
        "ikp_id": 1,
        "date_create": datetime(2024, 1, 2, 23),
        "date_begin": datetime(2024, 1, 2, 23),
        "date_end": datetime(2024, 1, 3, 20),
        "first_name": "VASYA",
        "second_name": "PETROVICH",
        "last_name": "MUROV",
        "date_of_birth": datetime(2024, 1, 2),
        "name": "OOO FOOTBALL",
        "inn": 123213,
        "lob_id": 1,
        "rate": 112.25,
    }


@pytest.fixture
def returning_face_data() -> dict[str, str | int]:
    return {
        "id": 1,
        "type": "legal",
        "first_name": "VASYA",
        "second_name": "PETROVICH",
        "last_name": "MUROV",
        "date_of_birth": datetime(2024, 1, 2),
        "name": "OOO FOOTBALL",
        "inn": 123213,
    }


@pytest.fixture
def returning_agent_agreements_data() -> dict[str, str | int | float]:
    return {
        "id": 1,
        "agent_id": 1,
        "lob_id": 1,
        "rate": 112.25,
    }


@pytest.fixture
def returning_ikp_data() -> dict[str, str | int]:
    return {
        "id": 1,
        "name": "VASKA",
    }
