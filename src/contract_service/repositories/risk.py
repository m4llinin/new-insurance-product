from src.core.database.base import SqlAlchemyRepository
from src.contract_service.models.risk import Risk


class RiskRepository(SqlAlchemyRepository, model=Risk):
    pass
