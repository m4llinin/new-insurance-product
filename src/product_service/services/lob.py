from typing import Any
from loguru import logger

from src.core.utils.base_service import BaseService
from src.product_service.utils.uow import ProductUOW
from src.core.cache.helper import CacheHelper


class LobService(BaseService):
    def __init__(self, uow: ProductUOW):
        self._uow = uow

    async def add(self, lob: dict[str, Any]) -> int:
        async with self._uow:
            lob_id = await self._uow.lobs.insert(lob)
            await self._uow.commit()
            return lob_id

    @CacheHelper.cache()
    async def get_lobs(self) -> list[dict[str, Any]]:
        async with self._uow:
            lobs = await self._uow.lobs.get_all({})
            logger.debug("Got lobs from database: {lobs}", lobs=lobs)
            return [lob.model_dump() for lob in lobs]
