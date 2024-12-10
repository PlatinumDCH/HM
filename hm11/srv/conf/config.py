from configparser import ConfigParser
from srv.conf.loging_conf import global_logger
import os

config_file_path = os.path.join(os.path.dirname(__file__),'config.ini')

class LoadConfig:
    def __init__(self, config_file=config_file_path):
        self.config_file = config_file
        self.parser = ConfigParser()
        self.parser.read(config_file)

        #load all parameters configuration
        self.load_pg_config()

    def load_pg_config(self):
        """Load the configuration from PostgresDB"""
        if self.parser.has_section('PG'):
            pg_config = dict(self.parser.items('PG'))
            db_url = f"{pg_config['driver']}://{pg_config['username']}:"\
                     f"{dict(pg_config)['password']}@"\
                     f"{pg_config['host']}:{pg_config['port']}/{pg_config['database']}"
            return db_url
        else:
            global_logger.error('Error read configuration for connection to Postgres')
            raise Exception("Section 'PG' not found.")

    def load_key_config(self):
        """Load secret key"""
        if self.parser.has_section('KEY'):
            key_config = dict(self.parser.items('KEY'))
            return key_config['secret_key']
        else:
            global_logger.error('Error read configuration for secret key')
            raise Exception("Section 'KEY' not found.")

    def load_algorithm_config(self):
        """Load algorithm configuration"""
        if self.parser.has_section('ALGO'):
            algorithm_config = dict(self.parser.items('ALGO'))
            return algorithm_config['algorithm']
        else:
            global_logger.error('Error read configuration for algorithm')
            raise Exception("Section 'ALGO' not found.")

    def load_mail_service_config(self):
        """Load configuration from mail service"""
        if self.parser.has_section('EMAIL SERVICE'):
            mail_config = dict(self.parser.items('EMAIL SERVICE'))
            return {
                'mail': mail_config['mail'],
                'password': mail_config['pass'],
                'port': int(mail_config['port']),
                'mail_server': mail_config['mail_server']
            }
        else:
            global_logger.error('Error read configuration for email service')
            raise Exception("Section 'EMAIL SERVICE' not found.")

    def load_rabbitmq_config(self):
        """Load configuration from RabbitMQ message broker"""
        if self.parser.has_section('rabbitmq'):
            rabbitmq_config = dict(self.parser.items('rabbitmq'))
            connection_url =  f"amqp://{rabbitmq_config['user']}:{rabbitmq_config['password']}@"\
                              f"{rabbitmq_config['host']}{rabbitmq_config['vhost']}"
            return connection_url
        else:
            global_logger.error('Error reading RabbitMQ configuration')
            raise Exception('Error reading RabbitMQ configuration')

object_load_config = LoadConfig()

class Config:
    DB_URL = object_load_config.load_pg_config()
    SECRET_KEY = object_load_config.load_key_config()
    ALGORITHM = object_load_config.load_algorithm_config()
    MAIL_CONF = object_load_config.load_mail_service_config()
    RABBITMQ_URL = object_load_config.load_rabbitmq_config()

configuration = Config






