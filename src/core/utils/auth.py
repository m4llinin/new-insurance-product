from faststream.rabbit.fastapi import RabbitBroker


async def check_auth(token: str, broker: RabbitBroker) -> bool:
    response = await broker.request(message={"token": token}, routing_key="auth-check")
    return response.decoded_body
