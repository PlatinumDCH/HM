from aio_pika import connect_robust, exceptions
from aio_pika.abc import AbstractRobustConnection
import asyncio

from srv.conf.config import configuration
from srv.conf.loging_conf import global_logger as logger

async def get_rabbitmq_connection(retries:int=5, delay:int=5)-> AbstractRobustConnection:
    rabbit_mq_url = configuration.RABBITMQ_URL
    for attempt in range(retries):
        try:
            connection = await connect_robust(rabbit_mq_url)
            logger.info("Successfully connected to RabbitMQ")
            return connection
        except exceptions.AMQPConnectionError as err:
            logger.warning(f'Connection failed (attempt {attempt + 1}/{retries}): {err}')
            await asyncio.sleep(delay)
    raise RuntimeError('Failed to connect to RabbitMQ after multiple attempts')