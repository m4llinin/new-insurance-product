from typing import Any

from loguru import logger

from src.core.utils.base_service import BaseService
from src.product_service.utils.uow import ProductUOW
from src.core.cache.helper import CacheHelper


class MetaFieldService(BaseService):
    def __init__(self, uow: ProductUOW):
        self._uow = uow

    @CacheHelper.cache()
    async def get_meta_fields(self) -> list[dict[str, Any]]:
        async with self._uow:
            meta_fields = await self._uow.meta_fields.get_all({})
            logger.debug(
                "Got meta_fields from database: {meta_fields}", meta_fields=meta_fields
            )
            return [meta_field.model_dump() for meta_field in meta_fields]

    async def insert_meta_fields(self, meta_fields: list[dict[str, Any]]) -> list[int]:
        result = []

        for meta_field in meta_fields:
            ins = await self.insert_meta_field(meta_field)
            if ins not in result:
                result.append(ins)

        return result

    async def insert_meta_field(self, meta_field: dict[str, Any]) -> int:
        async with self._uow:
            meta = await self._uow.meta_fields.get_one(meta_field)

            if meta is None:
                meta_id = await self._uow.meta_fields.insert(meta_field)
                logger.debug(
                    "Meta_field: {meta_field} was insert with id: {id}",
                    meta_field=meta_field,
                    id=meta_id,
                )
                await self._uow.commit()
                return meta_id

            return meta.id

    @CacheHelper.cache()
    async def get_metafield_rates(
        self, meta_fields: list[dict[str, Any]]
    ) -> list[float]:
        output_rates = []
        async with self._uow:
            for meta_field in meta_fields:
                meta_field_id = meta_field.get("id")
                meta_field_value = meta_field.get("value")

                meta_field_db = await self._uow.meta_fields.get_one(
                    {
                        "id": meta_field_id,
                    }
                )

                if meta_field_db is None:
                    raise ValueError(f"Metafield {meta_field_id} not found")

                if len(meta_field_db.possible_values) != 0:
                    possible_values = meta_field_db.possible_values
                    coefficients = meta_field_db.coefficients

                    index_coefficient = possible_values.index(meta_field_value)
                    output_rates.append(coefficients[index_coefficient])
                else:
                    output_rates.append(meta_field_db.constant_coefficient)
        logger.debug(
            "Got meta_field rates: {rates} for meta_fields: {meta_fields}",
            rates=output_rates,
            meta_fields=meta_fields,
        )
        return output_rates
