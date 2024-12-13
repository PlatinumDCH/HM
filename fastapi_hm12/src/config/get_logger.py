import logging
from pathlib import Path

LOG_FILE = '/Users/plarium/Develop/cources/Python_web/hm/fastapi_hm12/app.log'

def setup_logger()->logging.Logger:
    log_path = Path(LOG_FILE).parent
    log_path.mkdir(parents=True, exist_ok=True)

    #settings info logger
    formating = f'%(levelname)s - %(asctime)s  -%(filename)s - %(message)s'
    formatter = logging.Formatter(formating)

    handler = logging.FileHandler(LOG_FILE)
    handler.setFormatter(formatter)

    logger = logging.getLogger("global_logger")
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger

logger= setup_logger()