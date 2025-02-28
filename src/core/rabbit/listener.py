from typing import Type
from aio_pika.abc import (
    AbstractIncomingMessage,
    AbstractConnection,
    AbstractChannel,
    AbstractExchange,
)
from functools import wraps

from src.core.rabbit.base import BaseRabbit
from src.core.utils.singleton import singleton
from src.core.utils.uow import UnitOfWorkABC


@singleton
class ListenerRabbit(BaseRabbit):
    def __init__(self, url: str) -> None:
        self.consumers = []
        self.queues = {}
        super().__init__(url)

    def __call__(
        self,
        queue_name: str,
        uow: Type["UnitOfWorkABC"] | None = None,
    ):
        def decorator(func):
            @wraps(func)
            async def wrapper(message: AbstractIncomingMessage):
                async with message.process():
                    body = self.decode_body(message.body)

                    if not isinstance(body, dict):
                        raise TypeError(
                            f"Message body must be a dict, got {type(body)}"
                        )

                    if uow is not None:
                        body.update({"uow": uow()})

                    try:
                        response = await func(**body)
                    except (ValueError, TypeError):
                        response = None

                    if message.reply_to is not None:
                        await self.exchange.publish(
                            message=self.create_message(
                                body={
                                    "response": response,
                                },
                                correlation_id=message.correlation_id,
                            ),
                            routing_key=message.reply_to,
                        )

            self.consumers.append((queue_name, wrapper))
            return wrapper

        return decorator

    async def start(self) -> None:
        await self.connect()
        for queue_name, consumer in self.consumers:
            queue = await self.channel.declare_queue(queue_name)

            await queue.bind(self.exchange, routing_key=queue_name)
            await queue.consume(consumer)

            self.queues[queue_name] = queue
