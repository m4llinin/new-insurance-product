from src.core.utils.uow import UnitOfWork

from src.contract_service.repositories.risk import RiskRepository
from src.contract_service.repositories.contract import ContractRepository
from src.contract_service.repositories.contract_risks import ContractRiskRepository


class ContractUOW(UnitOfWork):
    async def __aenter__(self):
        await super().__aenter__()

        self.risks = RiskRepository(self.session)
        self.contracts = ContractRepository(self.session)
        self.contract_risks = ContractRiskRepository(self.session)
