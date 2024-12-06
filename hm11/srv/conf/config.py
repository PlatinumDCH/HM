from configparser import ConfigParser
from srv.conf.loging_conf import setup_logger
import os

config_file_path = os.path.join(os.path.dirname(__file__),'config.ini')
logger = setup_logger(__name__)

def load_config(config_file=config_file_path,section='PG'):
    parser = ConfigParser()
    parser.read(config_file)

    if parser.has_section(section):
        try:
            params = parser.items(section)
            return  {param[0]: param[1] for param in params}
        except Exception as e:
            logger.error(f"Error reading config section {section}: {e}")
            raise
    else:
        logger.error(f'Section {section} not found in {config_file}')
        raise Exception(f'Section {section} not found in {config_file}')

try:
    db_config = load_config()
    db_url = f"{db_config['driver']}://{db_config['username']}:{db_config['password']}@" \
             f"{db_config['host']}:{db_config['port']}/{db_config['database']}"
except Exception as err:
    logger.error(f'Failed to create DB URL: {err}')
    raise

try:
    key_config = load_config(section='KEY')
    SECRET_KEY = key_config['secret_key']
except Exception as err:
    logger.error(f'Failed to load secret key: {err}')
    raise

try:
    algorithm_config = load_config(section='ALGO')
    ALGORITHM = algorithm_config['algorithm']
except Exception as err:
    logger.error(f'Failed to load ALGORITHM: {err}')
    raise

class Config:
    DB_URL = db_url

config = Config

