from typing import Any

from fastapi.exceptions import RequestValidationError
from loguru import logger

from src.core.config import Config
from src.core.rabbit.listener import ListenerRabbit
from src.product_service.services.product import ProductService
from src.product_service.utils.uow import ProductUOW

listener = ListenerRabbit(Config().rmq.URL)


@listener("prod-get-products-without-metafields", uow=ProductUOW)
async def get_products_without_metafield(
    product_ids: list[int],
    uow: ProductUOW,
):
    logger.info(
        "Handling request for 'prod-get-products-without-metafields' with params: {params}",
        params=product_ids,
    )
    response = []

    try:
        response = await ProductService(uow).get_products_without_metafield(product_ids)
    except (ValueError, RequestValidationError):
        pass

    return response


@listener("prod-get-rates-products-and-metafields", uow=ProductUOW)
async def get_rates_products_and_metafield(
    product_id: int,
    meta_fields: list[dict[str, Any]],
    uow: ProductUOW,
):
    logger.info(
        "Handling request for 'prod-get-rates-products-and-metafields' with params: {params}",
        params=[product_id, meta_fields],
    )
    return await ProductService(uow).get_rates_product_and_metafield(
        product_id=product_id,
        meta_fields=meta_fields,
    )
