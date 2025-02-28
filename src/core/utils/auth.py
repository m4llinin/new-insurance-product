from pydantic import EmailStr

from src.core.rabbit.broker import BrokerRabbit


async def check_auth(
    token: str,
    broker: BrokerRabbit,
) -> bool:
    return await broker.request(
        message={
            "token": token,
        },
        routing_key="auth-check",
    )


async def get_auth_user(
    token: str,
    broker: BrokerRabbit,
) -> EmailStr:
    return await broker.request(
        message={
            "token": token,
        },
        routing_key="auth-get-user",
    )
