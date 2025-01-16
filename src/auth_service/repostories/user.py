from src.core.database.base import SqlAlchemyRepository
from src.auth_service.models.user import User


class UserRepository(SqlAlchemyRepository, model=User):
    pass
