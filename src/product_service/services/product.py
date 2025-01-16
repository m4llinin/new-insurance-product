from src.product_service.schemes.product import (
    ProductSchemeResponse,
    ProductSchemeRequest,
    ProductSchemeAddResponse,
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
            product = await self._uow.products.get_one({"id": product_id})

        meta_fields = await MetaFieldService(self._uow).get_meta_fields()
        product.meta_fields = list(
            filter(lambda meta_field: meta_field.id in product.meta_fields, meta_fields)
        )

        return product

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
