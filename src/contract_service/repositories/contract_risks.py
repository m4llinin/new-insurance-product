from src.core.database.base import SqlAlchemyRepository
from src.contract_service.models.contract_risks import ContractRisk


class ContractRiskRepository(SqlAlchemyRepository, model=ContractRisk):
    pass
