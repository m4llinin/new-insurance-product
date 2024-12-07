from typing import Annotated
from fastapi import Depends

from src.ProductService.utils.uow import ProductUOW

ProductUOWDep = Annotated[ProductUOW, Depends(ProductUOW)]
