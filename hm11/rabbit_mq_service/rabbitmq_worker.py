import asyncio
import json
from aio_pika import IncomingMessage, ExchangeType
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pathlib import Path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from srv.conf.config import configuration
from srv.conf.conn_rabbitMQ import get_rabbitmq_connection
from srv.services.auth import auth_service
from srv.conf.loging_conf import global_logger as logger

BASE_DIR = Path(__file__).resolve().parents[1]

#настройки для FastAPI Mail
conf = ConnectionConfig(
    MAIL_USERNAME=configuration.MAIL_USERNAME,
    MAIL_PASSWORD=configuration.MAIL_PASSWORD,
    MAIL_FROM=configuration.MAIL_USERNAME,
    MAIL_PORT=configuration.MAIL_PORT,
    MAIL_SERVER=configuration.MAIL_SERVER,
    MAIL_FROM_NAME='Contact server',
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=BASE_DIR / 'srv' / 'services' / 'templates'
)

async def process_message(message:IncomingMessage):
    """Обработка входящего сообщения из очереди"""
    try:
        async with message.process():
            task_data = json.loads(message.body)
            email = task_data['email']
            username = task_data['username']
            host = task_data['host']

            # создание токена для подтверждения email
            token_verification = auth_service.create_email_token({'sub':email})

           # формирование сообщения
            message_schema = MessageSchema(
                subject='Confirm your email',
                recipients=[email],
                template_body={'host':host, 'username':username,'token':token_verification},
                subtype=MessageType.html,
            )
            fm=FastMail(conf)
            await fm.send_message(message_schema, template_name='verify_email.html')
            logger.info(f'Message precessed successfully : {email}')
    except Exception as err:
        logger.error(f'Failed to process message: {err}')
        raise

async def main():
    """Основной воркер для обработки сообщений из RabbitMQ"""
    max_retires = 5 # максимальное количество повторных попыток
    retry_count = 0 # Счетчик попыток
    while retry_count < max_retires:
        try:
            connection = await get_rabbitmq_connection()

            # Объявление обменника
            async with connection:
                channel = await connection.channel()
                exchange = await channel.declare_exchange(
                        name="email_exchange",
                        type=ExchangeType.DIRECT,
                        durable=True
                    )

                # Объявление очереди
                queue = await channel.declare_queue('email_queue', durable=True)
                await queue.bind(exchange, routing_key="email_queue")
                await queue.consume(process_message)
                logger.info("Worker is consuming messages...")

                # Ожидание новых сообщений
                while True:
                    await asyncio.sleep(1)
        except Exception as err:
            retry_count += 1
            logger.error(f'An error occurred in the main loop: {err}')
            if retry_count < max_retires:
                logger.info(f'Retrying in 5 seconds... Attempt {retry_count}/{max_retires}')
                await asyncio.sleep(5)
            else:
                logger.critical('Max retry attempts reached.Exiting')
if __name__ == '__main__':
    asyncio.run(main())

