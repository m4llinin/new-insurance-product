from pydantic import BaseModel

from src.ProductService.schemes.metafields import MetaFieldScheme, MetaFieldSchemeRequest


class ProductScheme(BaseModel):
    id: int
    name: str
    lob_id: int
    basic_rate: float
    meta_fields: list[int] | None


class ProductSchemeAddResponse(BaseModel):
    id: int


class ProductSchemeResponse(BaseModel):
    id: int
    name: str
    lob_id: int
    basic_rate: float
    meta_fields: list[MetaFieldScheme] | None


class ProductSchemeRequest(BaseModel):
    name: str
    lob_id: int
    basic_rate: float
    meta_fields: list[MetaFieldSchemeRequest] | None
