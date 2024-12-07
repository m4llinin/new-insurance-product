from src.ProductService.utils.uow import ProductUOW
from src.ProductService.schemes.lobs import LobScheme


class LobService:
    def __init__(self, uow: ProductUOW):
        self._uow = uow

    async def get_lobs(self) -> list[LobScheme]:
        async with self._uow:
            return await self._uow.lobs.get_all({})
