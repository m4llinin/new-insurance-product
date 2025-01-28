from src.core.database.base import SqlAlchemyRepository
from src.agent_service.models.agent_agreements import AgentAgreements


class AgentAgreementsRepository(SqlAlchemyRepository, model=AgentAgreements):
    pass
