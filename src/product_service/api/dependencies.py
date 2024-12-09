from typing import Annotated
from fastapi import Depends

from src.product_service.utils.uow import ProductUOW

ProductUOWDep = Annotated[ProductUOW, Depends(ProductUOW)]
