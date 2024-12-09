from fastapi import APIRouter, HTTPException
from fastapi import status

from src.product_service.schemes.lob import LobScheme
from src.product_service.schemes.metafield import MetaFieldScheme
from src.product_service.schemes.product import ProductSchemeResponse, ProductSchemeRequest, ProductSchemeAddResponse

from src.product_service.services.lob import LobService
from src.product_service.services.product import ProductService
from src.product_service.services.metafield import MetaFieldService

from src.product_service.api.dependencies import ProductUOWDep

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
    try:
        return await ProductService(uow).add_product(product)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid values being passed"
        )


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
