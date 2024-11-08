from mongoengine import connect
from configuration.connect import uri

def connect_to_db():
    connect(
        db='web-16',
        host=uri,
    )