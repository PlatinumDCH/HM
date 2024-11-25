import configparser
import os
from mongoengine import connect,disconnect,get_db
from pymongo import MongoClient
import psycopg2


config_file_path = os.path.join(os.path.dirname(__file__),'config.ini')
config = configparser.ConfigParser()
config.read(config_file_path)

mongo_user = config.get('DB', 'USER')
mongodb_pass = config.get('DB', 'PASS')
domain = config.get('DB', 'DOMAIN')
options = config.get('DB', 'OPTIONS')

uri = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/?{options}"

pg_dbname = config.get('Potgress', 'dbname')
pg_user = config.get('Potgress', 'user')
pg_pass = config.get('Potgress', 'password')
pg_host = config.get('Potgress', 'host')
pg_port = config.get('Potgress', 'port')


def postgres_connect():
    pg_conn = psycopg2.connect(
        dbname = pg_dbname,
        user = pg_user,
        password = pg_pass,
        host = pg_host,
        port = pg_port
    )
    return pg_conn


def connect_mongo():
    connect(
        db='hm',
        host=uri
    )
def connect_pymongo():
    client = MongoClient(uri)
    db = client['hm']
    return db

def disconnect_mogo(alias='default'):
    disconnect(alias=alias)

def test_connection():
    """check connection"""

    try:
        connect_mongo()
        db = get_db()
        server_info = db.client.server_info()
        print("MongoDB connection: TRUE")
        print("Information about server: ", server_info)

    except Exception as e:
        print(f"An unexpected error occurred while connecting to MongoDB: {e}")
        exit(1)
    finally:
        disconnect_mogo()

if __name__ == '__main__':
    test_connection()