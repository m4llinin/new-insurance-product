from src.core.database.base import SqlAlchemyRepository
from src.product_service.models import Lob


class LobRepository(SqlAlchemyRepository, model=Lob):
    pass
