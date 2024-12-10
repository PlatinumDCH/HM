import aio_pika
import json
from aio_pika import ExchangeType

from srv.conf.conn_rabbitMQ import get_rabbitmq_connection

async def publish_message(message: dict):
    connection = await get_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()

        # Объявляем обменник, если его еще нет
        exchange = await channel.declare_exchange(
            name="email_exchange",
            type=ExchangeType.DIRECT,
            durable=True
        )

        # Публикуем сообщение в обменник
        await exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key='email_queue'
        )
