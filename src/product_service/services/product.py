from typing import Any

from src.product_service.schemes.product import (
    ProductSchemeResponse,
    ProductSchemeRequest,
    ProductSchemeAddResponse,
    ProductStatisticsScheme,
    RatesProduct,
    RatesProductResponse,
)
from src.product_service.utils.uow import ProductUOW
from src.product_service.services.metafield import MetaFieldService


class ProductService:
    def __init__(self, uow: ProductUOW):
        self._uow = uow

    async def get_products(self) -> list[ProductSchemeResponse]:
        async with self._uow:
            products = await self._uow.products.get_all({})
        meta_fields = await MetaFieldService(self._uow).get_meta_fields()

        for product in products:
            product.meta_fields = list(
                filter(
                    lambda meta_field: meta_field.id in product.meta_fields, meta_fields
                )
            )

        return products

    async def get_product(self, product_id: int) -> ProductSchemeResponse:
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

        return product

    async def get_products_without_metafield(
        self, product_ids: list[int]
    ) -> list[ProductStatisticsScheme]:
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
        return products

    async def add_product(
        self, product: ProductSchemeRequest
    ) -> ProductSchemeAddResponse:
        product_dict = product.model_dump()
        product_dict["meta_fields"] = await MetaFieldService(
            self._uow
        ).insert_meta_fields(product_dict["meta_fields"])

        async with self._uow:
            ins = await self._uow.products.insert(product_dict)
            await self._uow.commit()
        return ProductSchemeAddResponse(id=ins)

    async def get_rates_product_and_metafield(
        self, product: RatesProduct
    ) -> RatesProductResponse:
        product_dict = product.model_dump()
        meta_fields = await MetaFieldService(self._uow).get_metafield_rates(
            product_dict.get("meta_fields")
        )

        async with self._uow:
            product_db = await self._uow.products.get_one(
                {
                    "id": product.product_id,
                }
            )

        return RatesProductResponse(
            product_rate=product_db.basic_rate,
            meta_fields=meta_fields,
        )
