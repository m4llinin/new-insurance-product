from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import (
    FastAPI,
    APIRouter,
)
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import Config
from src.core.rabbit.broker import Broker
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
    routers: list[APIRouter] = [
        auth_router,
        rmq_auth_router,
        product_router,
        rmq_product_router,
        contract_router,
        agent_router,
        rmq_agent_router,
    ]

    def __init__(self, config: Config) -> None:
        self._config = config

    def setup_cors(self, app: FastAPI) -> None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=self._config.api.CORS_ORIGINS,
            allow_credentials=self._config.api.CORS_CREDENTIALS,
            allow_methods=self._config.api.CORS_METHODS,
            allow_headers=self._config.api.CORS_HEADERS,
        )

    def include_routers(self, app: FastAPI) -> None:
        for router in self.routers:
            app.include_router(router)

    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncGenerator[None, None]:
        broker = Broker(
            url=self._config.rmq.URL,
        )
        await broker.connect()

        DBConnection(
            url=self._config.db.URL,
        )
        CacheHelper.initialize(
            url=self._config.redis.URL,
        )

        yield

        await broker.disconnect()
        await CacheHelper.close()

    def initialize(self) -> FastAPI:
        app = FastAPI(lifespan=self.lifespan)
        setup_logging(
            mode=self._config.api.MODE,
            config=self._config.log,
        )
        self.setup_cors(app)
        self.include_routers(app)
        return app


app = App(config=Config()).initialize()
