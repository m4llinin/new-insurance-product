import asyncio
import json
from abc import (
    ABC,
    abstractmethod,
)
from typing import Any
from aio_pika import (
    Message,
    connect,
)
from aio_pika.abc import (
    AbstractConnection,
    AbstractChannel,
    AbstractMessage,
    AbstractExchange,
)


class RabbitABC(ABC):
    @staticmethod
    @abstractmethod
    def create_message(
        body: dict[str, Any],
        correlation_id: str = None,
        reply_to: str = None,
    ) -> AbstractMessage:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def decode_body(body: bytes) -> dict[str, Any]:
        raise NotImplementedError()

    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def disconnect(self) -> None:
        raise NotImplementedError()


class BaseRabbit(RabbitABC):
    def __init__(self, url: str) -> None:
        self.url = url
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None
        self.exchange: AbstractExchange | None = None

    @staticmethod
    def create_message(
        body: dict[str, Any],
        correlation_id: str = None,
        reply_to: str = None,
    ) -> AbstractMessage:
        return Message(
            body=json.dumps(body).encode(),
            correlation_id=correlation_id,
            reply_to=reply_to,
        )

    @staticmethod
    def decode_body(body: bytes) -> dict[str, Any]:
        return json.loads(body.decode())

    async def connect(self) -> None:
        self.connection = await connect(
            url=self.url,
            loop=asyncio.get_running_loop(),
        )
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.get_exchange("amq.direct")

    async def disconnect(self) -> None:
        if self.connection:
            await self.connection.close()
