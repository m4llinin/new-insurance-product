import json
from typing import Callable, ParamSpec, TypeVar, Any
from redis.asyncio import Redis
from functools import wraps


P = ParamSpec("P")
T = TypeVar("T")


class CacheHelper:
    _client: Redis = None

    @classmethod
    def initialize(cls, url: str):
        if cls._client is not None:
            raise RuntimeError("Cache pool is already initialized")
        cls._client = Redis.from_url(url)

    @classmethod
    async def close(cls):
        if cls._client is not None:
            await cls._client.aclose()

    @classmethod
    def cache(cls, ttl: int = 3600, prefix: str = None) -> Callable[P, T]:
        def decorator(func: Callable[P, T]) -> Callable[P, T]:
            @wraps(func)
            async def wrapper(*args, **kwargs) -> Any:
                if cls._client is None:
                    raise RuntimeError("Cache client is not initialized")

                key_prefix = prefix or func.__name__
                key = f"{key_prefix}:{[str(p) for p in args]}:{kwargs}"
                print(key)

                cached_value = await cls._client.get(key)

                if cached_value is not None:
                    return json.loads(cached_value)

                result = await func(*args, **kwargs)
                await cls._client.set(
                    name=key,
                    value=json.dumps(result, default=str),
                    ex=ttl,
                )
                return result

            return wrapper

        return decorator
