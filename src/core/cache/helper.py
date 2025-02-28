import json
from typing import (
    Callable,
    ParamSpec,
    TypeVar,
)

from loguru import logger
from redis.asyncio import Redis
from functools import wraps


P = ParamSpec("P")
T = TypeVar("T")


class CacheHelper:
    _client: Redis = None

    @classmethod
    def connect(cls, url: str):
        if cls._client is not None:
            raise RuntimeError("Cache pool is already initialized")
        cls._client = Redis.from_url(url)

    @classmethod
    async def disconnect(cls):
        if cls._client is not None:
            await cls._client.aclose()

    @classmethod
    def cache(cls, ttl: int = 3600, prefix: str = None) -> Callable[P, T]:
        def decorator(func: Callable[P, T]) -> Callable[P, T]:
            @wraps(func)
            async def wrapper(*args, **kwargs) -> T:
                if cls._client is None:
                    raise RuntimeError("Cache client is not initialized")

                key_prefix = prefix or func.__name__
                key = f"{key_prefix}:{[str(p) for p in args]}:{kwargs}"
                cached_value = await cls._client.get(key)

                if cached_value is not None:
                    data = json.loads(cached_value)
                    logger.info(
                        "Return value from cache with params: {params}",
                        params=[args, kwargs],
                    )
                    return data

                result = await func(*args, **kwargs)
                await cls._client.set(
                    name=key,
                    value=json.dumps(result, default=str),
                    ex=ttl,
                )
                return result

            return wrapper

        return decorator
