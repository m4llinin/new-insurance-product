import pytest
from unittest.mock import AsyncMock
from datetime import datetime

from src.contract_service.repositories.contract import ContractRepository
from src.contract_service.repositories.contract_risks import ContractRiskRepository
from src.contract_service.repositories.risk import RiskRepository


@pytest.fixture
def contract_repository(mock_async_session: AsyncMock) -> ContractRepository:
    return ContractRepository(session=mock_async_session)


@pytest.fixture
def contract_risk_repository(mock_async_session: AsyncMock) -> ContractRiskRepository:
    return ContractRiskRepository(session=mock_async_session)


@pytest.fixture
def risk_repository(mock_async_session: AsyncMock) -> RiskRepository:
    return RiskRepository(session=mock_async_session)


@pytest.fixture
def contract_data() -> dict[str, str | int]:
    return {
        "product_id": 1,
        "date_create": datetime(2024, 1, 4),
        "date_sign": datetime(2024, 1, 4),
        "date_begin": datetime(2024, 1, 4),
        "date_end": datetime(2025, 1, 4),
        "premium": 123.54,
        "insurance_sum": 123.54,
        "policy_price": 12365.0,
        "agent_id": 1,
        "rate": 123.56,
        "commission": 154.76,
        "status": "DRAFT",
        "policy_holder_id": 1,
        "insured_personal_id": 1,
        "owner_id": 1,
        "risk_id": None,
    }


@pytest.fixture
def returning_contract_data() -> dict[str, str | int]:
    return {
        "id": 1,
        "product_id": 1,
        "date_create": datetime(2024, 1, 4),
        "date_sign": datetime(2024, 1, 4),
        "date_begin": datetime(2024, 1, 4),
        "date_end": datetime(2025, 1, 4),
        "premium": 123.54,
        "insurance_sum": 123.54,
        "policy_price": 12365.0,
        "agent_id": 1,
        "rate": 123.56,
        "commission": 154.76,
        "status": "DRAFT",
        "policy_holder_id": 1,
        "insured_personal_id": 1,
        "owner_id": 1,
    }


@pytest.fixture
def returning_contract_data_list() -> list[dict[str, str | int]]:
    return [
        {
            "id": 1,
            "product_id": 1,
            "date_create": datetime(2024, 1, 4),
            "date_sign": datetime(2024, 1, 4),
            "date_begin": datetime(2024, 1, 4),
            "date_end": datetime(2025, 1, 4),
            "premium": 123.54,
            "insurance_sum": 123.54,
            "policy_price": 12365.0,
            "agent_id": 1,
            "rate": 123.56,
            "commission": 154.76,
            "status": "DRAFT",
            "policy_holder_id": 1,
            "insured_personal_id": 1,
            "owner_id": 1
        },
        {
            "id": 2,
            "product_id": 1,
            "date_create": datetime(2024, 1, 4),
            "date_sign": datetime(2024, 1, 4),
            "date_begin": datetime(2024, 1, 4),
            "date_end": datetime(2025, 1, 4),
            "premium": 123.54,
            "insurance_sum": 123.54,
            "policy_price": 12365.0,
            "agent_id": 1,
            "rate": 123.56,
            "commission": 154.76,
            "status": "SIGNED",
            "policy_holder_id": 1,
            "insured_personal_id": 1,
            "owner_id": 1,
        },
    ]


@pytest.fixture
def contract_risk_data() -> dict[str, str | int]:
    return {
        "contract_id": 1,
        "risk_id": [
            1,
            2,
            3,
        ],
        "premium": 123.54,
        "insurance_sum": 123.54,
    }


@pytest.fixture
def returning_contract_risk_data() -> dict[str, str | int]:
    return {
        "id": 1,
        "contract_id": 1,
        "risk_id": [
            1,
            2,
            3,
        ],
        "premium": 123.54,
        "insurance_sum": 123.54,
    }


@pytest.fixture
def returning_contract_risk_data_list() -> list[dict[str, str | int]]:
    return [
        {
            "id": 1,
            "contract_id": 1,
            "risk_id": [
                1,
                2,
                3,
            ],
            "premium": 123.54,
            "insurance_sum": 123.54,
        },
        {
            "id": 2,
            "contract_id": 2,
            "risk_id": [
                1,
                2,
            ],
            "premium": 187.54,
            "insurance_sum": 16786.54,
        },
    ]


@pytest.fixture
def risk_data() -> dict[str, str | int]:
    return {
        "name": "PENSIA",
        "rate": 123.54,
    }


@pytest.fixture
def returning_risk_data() -> dict[str, str | int]:
    return {
        "id": 1,
        "name": "PENSIA",
        "rate": 123.54,
    }


@pytest.fixture
def returning_risk_data_list() -> list[dict[str, str | int]]:
    return [
        {
            "id": 1,
            "name": "PENSIA",
            "rate": 123.54,
        },
        {
            "id": 2,
            "name": "POZAR",
            "rate": 178.54,
        },
    ]
