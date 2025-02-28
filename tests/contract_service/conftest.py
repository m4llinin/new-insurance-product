import pytest

from src.contract_service.utils.uow import ContractUOW


@pytest.fixture
def contract_uow() -> ContractUOW:
    return ContractUOW()
