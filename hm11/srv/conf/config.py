from dotenv import load_dotenv
import os

load_dotenv()
class Config:
    DB_URL = f"{os.getenv('PG_DRIVER')}://{os.getenv('PG_USERNAME')}:" \
             f"{os.getenv('PG_PASSWORD')}@{os.getenv('PG_HOST')}:" \
             f"{os.getenv('PG_PORT')}/{os.getenv('PG_DATABASE')}"
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = os.getenv('ALGORITHM')
    MAIL_CONF = {
        'mail': os.getenv('MAIL'),
        'password': os.getenv('MAIL_PASSWORD'),
        'port': int(os.getenv('MAIL_PORT')),
        'mail_server': os.getenv('MAIL_SERVER')
    }
    RABBITMQ_URL = f"amqp://{os.getenv('RABBITMQ_USER')}:{os.getenv('RABBITMQ_PASSWORD')}@" \
                   f"{os.getenv('RABBITMQ_HOST')}{os.getenv('RABBITMQ_VHOST')}"

configuration = Config()






