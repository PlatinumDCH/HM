import configparser
import os
from mongoengine import connect

config_file_path = os.path.join(os.path.dirname(__file__),'config.ini')
config = configparser.ConfigParser()
config.read(config_file_path)

mongo_user = config.get('DB', 'USER')
mongodb_pass = config.get('DB', 'PASS')
domain = config.get('DB', 'DOMAIN')
options = config.get('DB', 'OPTIONS')

uri = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/?{options}"


def connect_mongo():
    connect(
        db='hm',
        host=uri
    )

