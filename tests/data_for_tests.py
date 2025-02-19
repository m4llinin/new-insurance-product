from datetime import datetime
from typing import Any

from src.agent_service.services.agent import AgentService
from src.agent_service.services.agent_agreements import AgentAgreementsService
from src.agent_service.services.face import FaceService
from src.agent_service.services.ikp import IkpService
from src.agent_service.utils.uow import AgentUOW
from src.contract_service.services.risk import RiskService
from src.contract_service.utils.uow import ContractUOW
from src.product_service.services.lob import LobService
from src.product_service.utils.uow import ProductUOW
from src.agent_service.models import (
    Agent,
    AgentAgreements,
    Face,
    Ikp,
)
from src.auth_service.models import User
from src.contract_service.models import (
    Contract,
    ContractRisk,
    Risk,
)
from src.product_service.models import (
    Product,
    Lob,
    MetaField,
)


def get_ikps() -> list[dict[str, Any]]:
    return [
        {
            "name": "VASILEOSTROVSKAYA",
        },
        {
            "name": "PIONERSKAYA",
        },
        {
            "name": "PETROGRADSKAYA",
        },
    ]


def get_lobs() -> list[dict[str, Any]]:
    return [
        {
            "name": "CAR",
        },
        {
            "name": "FLOAT",
        },
        {
            "name": "HOUSE",
        },
    ]


def get_risks() -> list[dict[str, Any]]:
    return [
        {
            "name": "FLOOD",
        },
        {
            "name": "FIRE",
        },
        {
            "name": "EARTHQUAKE",
        },
    ]


def get_faces() -> list[dict[str, Any]]:
    return [
        {
            "type": "legal",
            "first_name": "ALEX",
            "second_name": "DMITRIEVICH",
            "last_name": "MITASOV",
            "date_of_birth": datetime(2005, 1, 1),
            "name": "VERTEX",
            "inn": 2343245,
        },
        {
            "type": "natural",
            "first_name": "DMITRIY",
            "second_name": "ALEXEVICH",
            "last_name": "TOPININ",
            "date_of_birth": datetime(2005, 5, 23),
            "inn": 14324512,
        },
        {
            "type": "natural",
            "first_name": "EGOR",
            "second_name": "ANATOLIEVICH",
            "last_name": "PANIN",
            "date_of_birth": datetime(1945, 9, 15),
            "inn": 12421432,
        },
    ]


def get_agents() -> list[dict[str, Any]]:
    return [
        {
            "face_id": 2,
            "ikp_id": 3,
            "status": "project",
            "date_create": datetime(2025, 10, 19, 20, 56, 30),
            "email": "example@email.ru",
        },
        {
            "face_id": 1,
            "ikp_id": 2,
            "status": "active",
            "date_create": datetime(2024, 7, 30, 15, 35),
            "date_begin": datetime(2024, 7, 30, 15, 50),
            "email": "example@email.com",
        },
        {
            "face_id": 3,
            "ikp_id": 1,
            "status": "terminated",
            "date_create": datetime(2023, 6, 22, 13, 43),
            "date_begin": datetime(2023, 6, 22, 13, 43),
            "date_end": datetime(2024, 6, 22, 13, 43),
            "email": "example@email.ya",
        },
    ]


def get_agent_agreements() -> list[dict[str, Any]]:
    return [
        {
            "agent_id": 1,
            "lob_id": 2,
            "rate": 23,
        },
        {
            "agent_id": 2,
            "lob_id": 3,
            "rate": 27,
        },
        {
            "agent_id": 3,
            "lob_id": 1,
            "rate": 89,
        },
    ]


async def add_ikps(
    ikps: list[dict[str, Any]] = None,
    agent_uow: AgentUOW = AgentUOW(),
) -> None:
    ikps = ikps or get_ikps()
    service = IkpService(agent_uow)
    for ikp in ikps:
        await service.add(ikp)


async def add_lobs(
    lobs: list[dict[str, Any]] = None,
    product_uow: ProductUOW = ProductUOW(),
) -> None:
    lobs = lobs or get_lobs()
    service = LobService(product_uow)
    for lob in lobs:
        await service.add(lob)


async def add_risks(
    risks: list[dict[str, Any]] = None,
    contract_uow: ContractUOW = ContractUOW(),
) -> None:
    risks = risks or get_risks()
    service = RiskService(contract_uow)
    for risk in risks:
        await service.add(risk)


async def add_faces(
    faces: list[dict[str, Any]] = None,
    agent_uow: AgentUOW = AgentUOW(),
) -> None:
    faces = faces or get_faces()
    service = FaceService(agent_uow)
    for face in faces:
        await service.add(face)


async def add_agents(
    agents: list[dict[str, Any]] = None,
    agent_uow: AgentUOW = AgentUOW(),
) -> None:
    agents = agents or get_agents()
    service = AgentService(agent_uow)
    for agent in agents:
        await service.add(agent)


async def add_agent_agreements(
    agent_agreements: list[dict[str, Any]] = None,
    agent_uow: AgentUOW = AgentUOW(),
) -> None:
    agent_agreements = agent_agreements or get_agent_agreements()
    service = AgentAgreementsService(agent_uow)
    for agent_agreement in agent_agreements:
        await service.add(agent_agreement)
