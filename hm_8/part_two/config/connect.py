import configparser
import os
from mongoengine import connect,disconnect
import pika

config_file_path = os.path.join(os.path.dirname(__file__),'config.ini')
config = configparser.ConfigParser()
config.read(config_file_path)

mongo_user = config.get('DB', 'USER')
mongodb_pass = config.get('DB', 'PASS')
domain = config.get('DB', 'DOMAIN')
options = config.get('DB', 'OPTIONS')

uri = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/?{options}"

q_email = 'email_queue'
q_sms = 'sms_queue'

rabbitmq_log = config.get('RabbitMQ','LOGGING')
rabbitmq_pass = config.get('RabbitMQ','PASSWORD')
rabbitmq_host = config.get('RabbitMQ','HOST')
rabbitmq_port = config.get('RabbitMQ','PORT')


def connect_mongo():
    connect(
        db='web-16',
        host=uri
    )
def disconnect_mogo(alias='default'):
    disconnect(alias=alias)

#connect to  RabbitMQ
credentials = pika.PlainCredentials(rabbitmq_log,rabbitmq_pass)
connRabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(
    host=rabbitmq_host, port=rabbitmq_port, credentials=credentials
))
