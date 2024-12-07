from src.core.database.base import SqlAlchemyRepository
from src.ProductService.models.lob import Lob


class LobRepository(SqlAlchemyRepository):
    model = Lob
