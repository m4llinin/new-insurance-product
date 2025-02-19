import asyncio
from functools import wraps

from aio_pika import connect, Message
from faststream.rabbit.broker import RabbitBroker

from src.core.utils.singleton import singleton


# @singleton
# class Broker:
#     def __init__(self, url: str = None) -> None:
#         self.url = url
#         if self.url is None:
#             raise ValueError("Broker url cannot be None")
#
#         self._broker = RabbitBroker(url=url)
#         self.is_connected = False
#
#     async def connect(self) -> None:
#         if self.is_connected:
#             return
#
#         await self._broker.connect()
#         await self._broker.start()
#         self.is_connected = True
#
#     async def disconnect(self) -> None:
#         if not self.is_connected:
#             return
#
#         await self._broker.close()
#         self.is_connected = False
#
#     @property
#     def broker(self) -> RabbitBroker:
#         if not self.is_connected:
#             raise RuntimeError("Broker not connected")
#         return self._broker


@singleton
class BrokerDecorator:
    tasks = []

    def __init__(self, url: str):
        self.url = url

    def __call__(self, queue_name: str):
        def decorator(func):
            @wraps(func)
            async def wrapper():
                connection = await connect(self.url)
                async with connection:
                    channel = await connection.channel()
                    await channel.set_qos(prefetch_count=1)

                    queue = await channel.declare_queue(queue_name, durable=True)
                    print(f"Listening to queue: {queue_name}")

                    await queue.consume(func)

                    async with queue.iterator() as queue_iter:
                        async for message in queue_iter:
                            message = await message
                            async with message.process():
                                token = message.body.decode()
                                print(
                                    f"Received token from queue '{queue_name}': {token}"
                                )

                                # Обрабатываем запрос через декорированную функцию
                                response = await func(token)

                                # Отправляем результат обратно в очередь ответа
                                if message.reply_to:
                                    await channel.default_exchange.publish(
                                        message=Message(
                                            body=response.encode(),
                                        ),
                                        routing_key=message.reply_to,
                                    )
                                    print(
                                        f"Sent response to reply_to queue: {message.reply_to}"
                                    )

            self.tasks.append(wrapper)
            return wrapper

        return decorator

    async def start_consumers(self):
        await asyncio.gather(*(task() for task in self.tasks))
