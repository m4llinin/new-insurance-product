from fastapi.exceptions import RequestValidationError
from faststream.rabbit.fastapi import RabbitRouter

from src.core.config import Config
from src.product_service.api.dependencies import ProductUOWDep
from src.product_service.schemes.product import (
    ProductStatisticsScheme,
    RatesProduct,
    RatesProductResponse,
)
from src.product_service.services.product import ProductService

router = RabbitRouter(Config().rmq.url())


@router.subscriber("prod-get-products-without-metafields")
async def get_products_without_metafield(
    uow: ProductUOWDep,
    product_ids: list[int],
) -> list[ProductStatisticsScheme]:
    response = []

    try:
        response = await ProductService(uow).get_products_without_metafield(product_ids)
    except (ValueError, RequestValidationError):
        pass

    return response


@router.subscriber("prod-get-rates-products-and-metafields")
async def get_rates_products_and_metafield(
    uow: ProductUOWDep,
    product: RatesProduct,
) -> RatesProductResponse:
    return await ProductService(uow).get_rates_product_and_metafield(product)
