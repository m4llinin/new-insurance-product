from fastapi import (
    APIRouter,
    HTTPException,
    status,
)
from loguru import logger

from src.product_service.schemes.lob import LobScheme
from src.product_service.schemes.metafield import MetaFieldScheme
from src.product_service.schemes.product import (
    ProductSchemeResponse,
    ProductSchemeRequest,
    ProductSchemeAddResponse,
)

from src.product_service.services.lob import LobService
from src.product_service.services.product import ProductService
from src.product_service.services.metafield import MetaFieldService

from src.product_service.api.dependencies import (
    ProductUOWDep,
    AuthDep,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[AuthDep],
)


@router.get("", response_model=list[ProductSchemeResponse])
async def get_products(uow: ProductUOWDep):
    logger.info("Handling request for GET '/products'")
    return await ProductService(uow).get_products()


@router.post("", response_model=ProductSchemeAddResponse)
async def add_product(
    uow: ProductUOWDep,
    product: ProductSchemeRequest,
):
    logger.info(
        "Handling request for POST '/products' with params: {params}", params=product
    )
    try:
        return await ProductService(uow).add_product(product)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid values being passed",
        )


@router.get("/lobs", response_model=list[LobScheme])
async def get_lobs(uow: ProductUOWDep):
    logger.info("Handling request for GET '/products/lobs'")
    return await LobService(uow).get_lobs()


@router.get("/meta_fields", response_model=list[MetaFieldScheme])
async def get_meta_fields(uow: ProductUOWDep):
    logger.info("Handling request for GET '/products/lobs'")
    return await MetaFieldService(uow).get_meta_fields()
