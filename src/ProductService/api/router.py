from fastapi import APIRouter

from src.ProductService.schemes.lobs import LobScheme
from src.ProductService.schemes.metafields import MetaFieldScheme
from src.ProductService.schemes.products import ProductSchemeResponse, ProductSchemeRequest, ProductSchemeAddResponse

from src.ProductService.services.lob import LobService
from src.ProductService.services.product import ProductService
from src.ProductService.services.metafield import MetaFieldService

from src.ProductService.api.dependencies import ProductUOWDep

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("")
async def get_products(
        uow: ProductUOWDep
) -> list[ProductSchemeResponse]:
    return await ProductService(uow).get_products()


@router.post("")
async def add_product(
        uow: ProductUOWDep,
        product: ProductSchemeRequest
) -> ProductSchemeAddResponse:
    return await ProductService(uow).add_product(product)


@router.get("/lobs")
async def get_lobs(
        uow: ProductUOWDep
) -> list[LobScheme]:
    return await LobService(uow).get_lobs()


@router.get("/meta_fields")
async def get_meta_fields(
        uow: ProductUOWDep
) -> list[MetaFieldScheme]:
    return await MetaFieldService(uow).get_meta_fields()
