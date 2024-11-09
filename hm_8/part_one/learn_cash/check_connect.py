import redis
try:
    client = redis.Redis(
        host='localhost',
        port=6379,
        password=None

    )
    client.ping()
    print('Connection [True]')

except redis.ConnectionError as err:
    print('Connection [False]', err)
