from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from src.product_service import router as product_router
from src.core.config import Config
from src.core.database.connection import DBConnection


class App:
    def __init__(self, config: Config, routers: list[APIRouter]):
        self._config = config
        self.app = FastAPI()
        self.routers = routers

    def setup_cors(self) -> None:
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self._config.api.CORS_ORIGINS,
            allow_credentials=self._config.api.CORS_CREDENTIALS,
            allow_methods=self._config.api.CORS_METHODS,
            allow_headers=self._config.api.CORS_HEADERS
        )

    def include_routers(self) -> None:
        for router in self.routers:
            self.app.include_router(router)

    def setup_app(self) -> FastAPI:
        DBConnection.create_instance(self._config.db.to_url())
        self.setup_cors()
        self.include_routers()
        return self.app


app = App(config=Config(),
          routers=[product_router, ]).setup_app()
