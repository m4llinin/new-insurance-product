from src.contract_service.utils.uow import ContractUOW
from src.contract_service.repositories.contract import ContractRepository
from src.contract_service.repositories.contract_risks import ContractRiskRepository
from src.contract_service.repositories.risk import RiskRepository


class TestContractUOW:
    async def test_contract_uow_initialization(
        self,
        contract_uow: ContractUOW,
    ) -> None:
        async with contract_uow:
            assert isinstance(contract_uow.contracts, ContractRepository)
            assert isinstance(contract_uow.contract_risks, ContractRiskRepository)
            assert isinstance(contract_uow.risks, RiskRepository)

    async def test_contract_uow_context_manager(
        self,
        contract_uow: ContractUOW,
    ) -> None:
        assert not hasattr(contract_uow, "contracts")
        assert not hasattr(contract_uow, "contract_risks")
        assert not hasattr(contract_uow, "risks")

        async with contract_uow:
            assert hasattr(contract_uow, "contracts")
            assert hasattr(contract_uow, "contract_risks")
            assert hasattr(contract_uow, "risks")
