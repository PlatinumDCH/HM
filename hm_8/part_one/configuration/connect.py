import configparser
import os
from mongoengine import connect
import redis

config_file_path = os.path.join(os.path.dirname(__file__),'config.ini')
config = configparser.ConfigParser()
config.read(config_file_path)

mongo_user = config.get('DB', 'USER')
mongodb_pass = config.get('DB', 'PASS')
domain = config.get('DB', 'DOMAIN')
options = config.get('DB', 'OPTIONS')

uri = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/?{options}"

redis_port = config.get('RD', 'PORT')
redis_host = config.get('RD', 'HOST')


def connect_mongo():
    connect(
        db='web-16',
        host=uri
    )
def connect_redis():
    client = redis.StrictRedis(
        host=redis_host,
        port=redis_port,
        password=None
    )
    return client
