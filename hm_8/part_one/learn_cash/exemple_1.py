import redis
from redis_lru import RedisLRU


client = redis.Redis(
        host='localhost',
        port=6379,
        password=None

    )
cache = RedisLRU(client)
@cache
def slow_function(x):
    print(f'Computing {x}...')
    import time
    time.sleep(2)
    return x * x


if __name__ == '__main__':
    print(slow_function(2))
    print(slow_function(2))
    print(slow_function(3))
    print(slow_function(3))