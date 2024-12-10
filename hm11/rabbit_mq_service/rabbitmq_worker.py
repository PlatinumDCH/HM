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

conf = ConnectionConfig(
    MAIL_USERNAME=configuration.MAIL_CONF['mail'],
    MAIL_PASSWORD=configuration.MAIL_CONF['password'],
    MAIL_FROM=configuration.MAIL_CONF['mail'],
    MAIL_PORT=configuration.MAIL_CONF['port'],
    MAIL_SERVER=configuration.MAIL_CONF['mail_server'],
    MAIL_FROM_NAME='Contact server',
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=BASE_DIR / 'srv' / 'services' / 'templates'
)

async def process_message(message:IncomingMessage):
    try:
        async with message.process():
            task_data = json.loads(message.body)
            email = task_data['email']
            username = task_data['username']
            host = task_data['host']

            token_verification = auth_service.create_email_token({'sub':email})
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
    while True:
        try:
            connection = await get_rabbitmq_connection()
            async with connection:
                channel = await connection.channel()
                exchange = await channel.declare_exchange(
                        name="email_exchange",
                        type=ExchangeType.DIRECT,
                        durable=True
                    )
                queue = await channel.declare_queue('email_queue', durable=True)
                await queue.bind(exchange, routing_key="email_queue")
                await queue.consume(process_message)
                logger.info("Worker is consuming messages...")
                while True:
                    await asyncio.sleep(1)
        except Exception as err:
            logger.error(f'An error occurred in the main loop: {err}')
            logger.info('Retrying in 5 seconds...')
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())

