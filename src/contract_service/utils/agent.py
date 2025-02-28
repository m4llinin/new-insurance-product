from pydantic import EmailStr

from src.core.cache.helper import CacheHelper
from src.core.rabbit.broker import BrokerRabbit


@CacheHelper.cache()
async def get_agent(
    email: EmailStr,
    column: str,
    broker: BrokerRabbit,
) -> int:
    return await broker.request(
        message={
            "email": email,
            "column": column,
        },
        routing_key="agent-get-agent",
    )
