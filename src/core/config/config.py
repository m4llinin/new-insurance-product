from typing import Annotated
from pydantic import AfterValidator

from src.core.config.base import BaseConfig

list_str = Annotated[str, AfterValidator(BaseConfig.parse_to_list)]


class DBConfig(BaseConfig):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_DATABASE: str

    def url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"


class RedisConfig(BaseConfig):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DATABASE: str

    def url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DATABASE}"


class AuthConfig(BaseConfig):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int


class ApiConfig(BaseConfig):
    CORS_ORIGINS: list_str
    CORS_CREDENTIALS: bool
    CORS_METHODS: list_str
    CORS_HEADERS: list_str


class RMQConfig(BaseConfig):
    RMQ_USERNAME: str
    RMQ_PASSWORD: str
    RMQ_HOST: str
    RMQ_PORT: int

    def url(self) -> str:
        return f"postgresql+asyncpg://{self.RMQ_USERNAME}:{self.RMQ_PASSWORD}@{self.RMQ_HOST}:{self.RMQ_PORT}"


class Config:
    IS_DEV: bool = True

    def __init__(self) -> None:
        self.db = DBConfig()
        self.auth = AuthConfig()
        self.rds = RedisConfig()
        self.api = ApiConfig()
        self.rmq = RMQConfig()
