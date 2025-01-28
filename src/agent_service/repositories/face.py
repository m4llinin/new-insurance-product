from src.core.database.base import SqlAlchemyRepository
from src.agent_service.models.face import Face


class FaceRepository(SqlAlchemyRepository, model=Face):
    pass
