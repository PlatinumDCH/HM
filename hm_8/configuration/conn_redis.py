import redis
from .connect import redis_host, redis_port

def connect_redis_db():
    client = redis.StrictRedis(
        host=redis_host,
        port=redis_port,
        password=None
    )
    return client