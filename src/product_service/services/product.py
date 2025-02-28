from typing import Any

from loguru import logger

from src.core.utils.base_service import BaseService
from src.product_service.schemes.product import (
    ProductSchemeRequest,
    ProductStatisticsScheme,
    RatesProduct,
)
from src.product_service.utils.uow import ProductUOW
from src.product_service.services.metafield import MetaFieldService
from src.core.cache.helper import CacheHelper


class ProductService(BaseService):
    def __init__(self, uow: ProductUOW):
        self._uow = uow

    @CacheHelper.cache()
    async def get_products(self) -> list[dict[str, Any]]:
        async with self._uow:
            products = await self._uow.products.get_all({})
        meta_fields = await MetaFieldService(self._uow).get_meta_fields()

        for product in products:
            product.meta_fields = list(
                filter(
                    lambda meta_field: meta_field.get("id") in product.meta_fields,
                    meta_fields,
                )
            )
        logger.debug("Got products from database: {products}", products=products)
        return [product.model_dump() for product in products]

    @CacheHelper.cache()
    async def get_product(self, product_id: int) -> dict[str, Any]:
        async with self._uow:
            product = await self._uow.products.get_one(
                {
                    "id": product_id,
                }
            )

        meta_fields = await MetaFieldService(self._uow).get_meta_fields()
        product.meta_fields = list(
            filter(lambda meta_field: meta_field.id in product.meta_fields, meta_fields)
        )
        logger.debug("Got product from database: {product}", product=product)
        return product.model_dump()

    @CacheHelper.cache()
    async def get_products_without_metafield(
        self, product_ids: list[int]
    ) -> list[dict[str, Any]]:
        products = []
        async with self._uow:
            for product_id in product_ids:
                product = await self._uow.products.get_one(
                    {
                        "id": product_id,
                    }
                )
                products.append(
                    ProductStatisticsScheme(
                        id=product.id,
                        name=product.name,
                    )
                )
        logger.debug(
            "Got products from database: {products} with ids: {ids}",
            products=products,
            ids=product_ids,
        )
        return [product.model_dump() for product in products]

    async def add_product(self, product: ProductSchemeRequest) -> dict[str, Any]:
        product_dict = product.model_dump()
        product_dict["meta_fields"] = await MetaFieldService(
            self._uow
        ).insert_meta_fields(product_dict["meta_fields"])

        async with self._uow:
            product_id = await self._uow.products.insert(product_dict)
            await self._uow.commit()
        logger.debug(
            "Product: {product} was insert with id: {id}",
            product=product,
            id=product_id,
        )
        return {
            "id": product_id,
        }

    @CacheHelper.cache()
    async def get_rates_product_and_metafield(
        self,
        product_id: int,
        meta_fields: list[dict[str, Any]],
    ) -> dict[str, Any]:
        meta_fields = await MetaFieldService(self._uow).get_metafield_rates(meta_fields)

        async with self._uow:
            product_db = await self._uow.products.get_one(
                {
                    "id": product_id,
                }
            )
        logger.debug(
            "Got product rates: {rates} with params: {params}",
            rates=product_db.basic_rate,
            params=product_id,
        )
        return {
            "product_rate": product_db.basic_rate,
            "meta_fields": meta_fields,
        }
