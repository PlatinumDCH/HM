from aio_pika import connect_robust, exceptions
from aio_pika.abc import AbstractRobustConnection
import asyncio

from src.config import settings, logger

async def get_rabbit_connection(retries:int=5, delay:int=5)->AbstractRobustConnection:
    for attempt in range(retries):
        try:
            connection = await connect_robust(
                settings.RABBITMQ_URL
            )
            logger.info('rabbitmq conn TRUE')
            return connection
        except exceptions.AMQPConnectionError as err:
            logger.error(f'rabbitmq conn FALSE, {attempt + 1}/{retries} {err}')
            await asyncio.sleep(delay)
        raise RuntimeError('Could not connect to RabbitMQ')