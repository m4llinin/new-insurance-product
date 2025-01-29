from typing import Any

from src.core.utils.base_service import BaseService
from src.product_service.utils.uow import ProductUOW
from src.product_service.schemes.lob import LobScheme
from src.core.cache.helper import CacheHelper

class LobService(BaseService):
    def __init__(self, uow: ProductUOW):
        self._uow = uow

    @CacheHelper.cache()
    async def get_lobs(self) -> list[dict[str, Any]]:
        async with self._uow:
            lobs = await self._uow.lobs.get_all({})
            return [lob.model_dump() for lob in lobs]
