from src.agent_service.api.router import router
from src.agent_service.api.rmq_router import router as rmq_router

__all__ = [
    "router",
    "rmq_router",
]
