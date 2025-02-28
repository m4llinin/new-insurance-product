import pytest
from datetime import datetime
from unittest.mock import AsyncMock

from src.agent_service.repositories.agent import AgentRepository
from src.agent_service.repositories.agent_agreements import AgentAgreementsRepository
from src.agent_service.repositories.face import FaceRepository
from src.agent_service.repositories.ikp import IkpRepository


@pytest.fixture
async def agent_repository(
    mock_async_session: AsyncMock,
) -> AgentRepository:
    return AgentRepository(session=mock_async_session)


@pytest.fixture
async def agent_agreements_repository(
    mock_async_session: AsyncMock,
) -> AgentAgreementsRepository:
    return AgentAgreementsRepository(session=mock_async_session)


@pytest.fixture
async def face_repository(
    mock_async_session: AsyncMock,
) -> FaceRepository:
    return FaceRepository(session=mock_async_session)


@pytest.fixture
async def ikp_repository(
    mock_async_session: AsyncMock,
) -> IkpRepository:
    return IkpRepository(session=mock_async_session)


@pytest.fixture
def returning_agent_data_list() -> list[dict[str, str | int | datetime]]:
    return [
        {
            "id": 1,
            "email": "example@email.com",
            "face_id": 1,
            "ikp_id": 1,
            "status": "active",
            "date_create": datetime(2024, 1, 2, 23),
            "date_begin": datetime(2024, 1, 2, 23),
            "date_end": datetime(2024, 1, 3, 20),
        },
        {
            "id": 2,
            "email": "example@email.ru",
            "face_id": 2,
            "ikp_id": 1,
            "status": "project",
            "date_create": datetime(2024, 1, 2, 23),
            "date_begin": datetime(2024, 1, 2, 23),
            "date_end": datetime(2024, 1, 3, 20),
        },
    ]


@pytest.fixture
def face_data() -> dict[str, str | int]:
    return {
        "type": "legal",
        "first_name": "VASYA",
        "second_name": "PETROVICH",
        "last_name": "MUROV",
        "date_of_birth": datetime(2024, 1, 2),
        "name": "OOO FOOTBALL",
        "inn": 123213,
    }


@pytest.fixture
def returning_face_data_list() -> list[dict[str, str | int]]:
    return [
        {
            "id": 1,
            "type": "legal",
            "first_name": "VASYA",
            "second_name": "PETROVICH",
            "last_name": "MUROV",
            "date_of_birth": datetime(2024, 1, 2),
            "name": "OOO FOOTBALL",
            "inn": 123213,
        },
        {
            "id": 2,
            "type": "natural",
            "first_name": "VASYA",
            "second_name": "PETROVICH",
            "last_name": "MUROV",
            "date_of_birth": datetime(2024, 1, 6),
            "inn": 123123,
        },
    ]


@pytest.fixture
def agent_agreements_data() -> dict[str, str | int | float]:
    return {
        "agent_id": 1,
        "lob_id": 1,
        "rate": 112.25,
    }


@pytest.fixture
def returning_agent_agreements_data_list() -> list[dict[str, str | int | float]]:
    return [
        {
            "id": 1,
            "agent_id": 1,
            "lob_id": 1,
            "rate": 112.25,
        },
        {
            "id": 2,
            "agent_id": 2,
            "lob_id": 2,
            "rate": 102.25,
        },
    ]


@pytest.fixture
def ikp_data() -> dict[str, str]:
    return {
        "name": "VASKA",
    }


@pytest.fixture
def returning_ikp_data_list() -> list[dict[str, str | int]]:
    return [
        {
            "id": 1,
            "name": "VASKA",
        },
        {
            "id": 2,
            "name": "PETROGA",
        },
    ]
