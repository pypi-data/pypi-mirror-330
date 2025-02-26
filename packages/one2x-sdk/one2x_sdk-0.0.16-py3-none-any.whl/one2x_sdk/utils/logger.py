import logging


def get_default_logger(name):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
