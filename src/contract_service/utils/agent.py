from faststream.rabbit import RabbitBroker
from pydantic import EmailStr


async def get_agent(
    email: EmailStr,
    column: str,
    broker: RabbitBroker,
) -> int:
    response = await broker.request(
        message={
            "email": email,
            "column": column,
        },
        routing_key="agent-get-agent",
    )
    return await response.decode()
