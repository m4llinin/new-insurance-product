import asyncio
import uuid
from typing import Any
from aio_pika.abc import AbstractIncomingMessage

from src.core.rabbit.base import BaseRabbit
from src.core.utils.singleton import singleton


@singleton
class BrokerRabbit(BaseRabbit):
    async def _publish(
        self,
        message: dict[str, Any],
        routing_key: str,
        correlation_id: str = None,
        reply_to: str = None,
    ) -> None:
        if not self.connection or self.connection.is_closed:
            raise RuntimeError("Rabbit is not connected")

        if not self.channel or self.channel.is_closed:
            raise RuntimeError("Rabbit has not channel")

        await self.exchange.publish(
            message=self.create_message(
                body=message,
                correlation_id=correlation_id,
                reply_to=reply_to,
            ),
            routing_key=routing_key,
        )

    async def publish(
        self,
        message: dict[str, Any],
        routing_key: str,
        reply_to: str = None,
    ) -> None:
        await self._publish(
            message=message,
            routing_key=routing_key,
            reply_to=reply_to,
        )

    async def request(
        self,
        message: dict[str, Any],
        routing_key: str,
    ) -> Any:
        correlation_id = str(uuid.uuid4())
        future = asyncio.get_running_loop().create_future()

        async def callback(callback_message: AbstractIncomingMessage):
            async with callback_message.process():
                future.set_result(
                    self.decode_body(callback_message.body),
                )

        if not self.channel or self.channel.is_closed:
            raise RuntimeError("Rabbit has not channel")

        reply_queue = await self.channel.declare_queue(
            name=correlation_id,
            auto_delete=True,
        )
        await reply_queue.bind(self.exchange, routing_key=correlation_id)
        await reply_queue.consume(callback)

        await self._publish(
            message=message,
            routing_key=routing_key,
            correlation_id=correlation_id,
            reply_to=reply_queue.name,
        )

        response = await future
        return response.get("response")
