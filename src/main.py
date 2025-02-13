from fastapi import (
    FastAPI,
    APIRouter,
)
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.core.config import Config
from src.core.database.connection import DBConnection
from src.core.cache.helper import CacheHelper
from src.core.log import setup_logging
from src.product_service import (
    router as product_router,
    rmq_router as rmq_product_router,
)
from src.auth_service import (
    router as auth_router,
    rmq_router as rmq_auth_router,
)
from src.contract_service import router as contract_router
from src.agent_service import (
    router as agent_router,
    rmq_router as rmq_agent_router,
)


class App:
    def __init__(
        self,
        *routers: APIRouter,
        config: Config,
    ):
        self._config = config
        self.app = FastAPI()
        self.routers = routers

    def setup_cors(self) -> None:
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self._config.api.CORS_ORIGINS,
            allow_credentials=self._config.api.CORS_CREDENTIALS,
            allow_methods=self._config.api.CORS_METHODS,
            allow_headers=self._config.api.CORS_HEADERS,
        )

    def include_routers(self) -> None:
        for router in self.routers:
            self.app.include_router(router)

    def setup_app(self) -> FastAPI:
        setup_logging(self._config.log)
        DBConnection.create_instance(url=self._config.db.url())
        CacheHelper.initialize(url=self._config.redis.url())
        self.setup_cors()
        self.include_routers()
        return self.app


app = App(
    product_router,
    rmq_product_router,
    auth_router,
    rmq_auth_router,
    contract_router,
    agent_router,
    rmq_agent_router,
    config=Config(),
).setup_app()
