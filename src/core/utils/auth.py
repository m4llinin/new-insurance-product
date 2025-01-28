from faststream.rabbit.fastapi import RabbitBroker
from pydantic import EmailStr


async def check_auth(
    token: str,
    broker: RabbitBroker,
) -> bool:
    response = await broker.request(
        message={
            "token": token,
        },
        routing_key="auth-check",
    )
    return await response.decode()


async def get_auth_user(
    token: str,
    broker: RabbitBroker,
) -> EmailStr:
    response = await broker.request(
        message={
            "token": token,
        },
        routing_key="auth-get-user",
    )
    return await response.decode()
