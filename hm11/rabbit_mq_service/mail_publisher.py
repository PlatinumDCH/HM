import aio_pika
import json
from aio_pika import ExchangeType

from srv.conf.conn_rabbitMQ import get_rabbitmq_connection
from srv.conf.loging_conf import global_logger as logger

async def publish_message(message: dict, queue_name: str):
    '''Публикация сообщения в RabbitMQ
    
    :parm message: Словарь с данными для публикации в RabbitMQ
    :parm message_type: Тип сообщения (password_reset, email_verification)
    '''
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
            routing_key=queue_name
        )
        logger.info(f"Message published to RabbitMQ with routing_key '{queue_name}': {message}")
