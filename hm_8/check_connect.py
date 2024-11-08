from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from configuration.connect import  uri


def check_mongo_connection(uri):
    try:
        client = MongoClient(
            uri,
            server_api=ServerApi("1"),
            # socketTimeoutMS=60000,
            # connectTimeoutMS=60000,
            # tls=True,  # Включить TLS/SSL
            # tlsAllowInvalidCertificates=True
        )

        client.admin.command('ping')
        print("Connect status [True]")
        client.close()
    except Exception as e:
        print(f"Connect status [False]: {e}")


if __name__ == '__main__':
    check_mongo_connection(uri)