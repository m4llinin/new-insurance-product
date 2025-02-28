import pytest
from unittest.mock import AsyncMock

from src.contract_service.services.contract import ContractService
from src.contract_service.services.contract_risks import ContractRiskService
from src.contract_service.services.risk import RiskService
from src.contract_service.utils.uow import ContractUOW


@pytest.fixture
def mock_uow() -> AsyncMock:
    uow = AsyncMock(spec=ContractUOW)
    uow.contract_risks = AsyncMock()
    uow.risks = AsyncMock()
    uow.contracts = AsyncMock()
    return uow


@pytest.fixture
def contract_risk_service(mock_uow):
    return ContractRiskService(mock_uow)


@pytest.fixture
def risk_service(mock_uow):
    return RiskService(mock_uow)


@pytest.fixture
def contract_service(mock_uow):
    return ContractService(mock_uow)
