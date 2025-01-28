from typing import Any

from src.product_service.utils.uow import ProductUOW
from src.product_service.schemes.metafield import MetaFieldScheme


class MetaFieldService:
    def __init__(self, uow: ProductUOW):
        self._uow = uow

    async def get_meta_fields(self) -> list[MetaFieldScheme]:
        async with self._uow:
            return await self._uow.meta_fields.get_all({})

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
                await self._uow.commit()
                return meta_id

            return meta.id

    async def get_metafield_rates(self, meta_fields: list[dict[str, Any]]) -> list:
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

        return output_rates
