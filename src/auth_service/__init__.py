from src.auth_service.api.routers import router
from src.auth_service.api.rmq_router import router as rmq_router

__all__ = ["router", "rmq_router"]
