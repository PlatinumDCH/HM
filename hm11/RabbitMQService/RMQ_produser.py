import json
from aio_pika import Message, DeliveryMode, ExchangeType
from srv.conf.conn_rabbitMQ import get_rabbitmq_connection

async def send_to_rabbitmq(message_data:dict, queue_name:str):
    connection = await get_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            name="email_exchange",
            type=ExchangeType.DIRECT,
            durable=True
        )
        await exchange.publish(
            Message(
                body=json.dumps(message_data).encode(),
                delivery_mode=DeliveryMode.PERSISTENT
            ),
            routing_key=queue_name,
        )