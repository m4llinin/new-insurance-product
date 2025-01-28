from src.core.database.base import SqlAlchemyRepository
from src.agent_service.models.ikp import Ikp


class IkpRepository(SqlAlchemyRepository, model=Ikp):
    pass
