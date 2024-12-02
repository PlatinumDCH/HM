import logging

def setup_logger(name:str, log_file:str = 'app.log')->logging.Logger:
    format = f'%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formater = logging.Formatter(format)

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formater)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger


