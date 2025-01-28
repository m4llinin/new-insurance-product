from src.product_service.api.routers import router
from src.product_service.api.rmq_router import router as rmq_router

__all__ = ["router", "rmq_router"]
