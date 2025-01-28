from pydantic import BaseModel

from src.product_service.schemes.metafield import (
    MetaFieldScheme,
    MetaFieldSchemeRequest,
)


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
    basic_rate: float = 1.0
    meta_fields: list[MetaFieldSchemeRequest] | None


class ProductStatisticsScheme(BaseModel):
    id: int
    name: str
    all_commission: float = 0
    all_premium: float = 0


class RatesMetaFieldScheme(BaseModel):
    id: int
    value: str | float


class RatesProduct(BaseModel):
    product_id: int
    meta_fields: list[RatesMetaFieldScheme]


class RatesProductResponse(BaseModel):
    product_rate: float
    meta_fields: list[float]
