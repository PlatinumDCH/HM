import configparser
import os
from mongoengine import connect,disconnect,get_db

config_file_path = os.path.join(os.path.dirname(__file__),'config.ini')
config = configparser.ConfigParser()
config.read(config_file_path)

mongo_user = config.get('DB', 'USER')
mongodb_pass = config.get('DB', 'PASS')
domain = config.get('DB', 'DOMAIN')
options = config.get('DB', 'OPTIONS')

uri = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/?{options}"

def connect_mongo():
    db = connect(
        db='hm',
        host=uri
    )
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