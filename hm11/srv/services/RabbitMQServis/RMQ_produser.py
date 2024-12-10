import aio_pika
import json
from aio_pika import Message, DeliveryMode

async def send_to_rabbitmq(message_data:dict, queue_name:str):
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel() # создаем канал
        await channel.default_exchange.publish(
            Message(
                body=json.dumps(message_data).encode(),
                delivery_mode=DeliveryMode.PERSISTENT #сообщения сохраняются при сбое RabbitMQ
            ),
            routing_key=queue_name,
        )