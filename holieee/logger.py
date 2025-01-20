import logging

logging.basicConfig(filename="logs/holieee.log",
                    format='%(levelname)s %(asctime)s %(message)s',
                    level=logging.DEBUG,
                    encoding='utf-8',
                    filemode='a')

logger = logging.getLogger('holieeelogging')

def log_debug(reason):
    logger.debug(reason)
    return

def log_info(reason):
    logger.info(reason)
    return

def log_warning(reason):
    logger.warning(reason)
    return

def log_error(reason):
    logger.error(reason)
    return

def log_critical(reason):
    logger.critical(reason)
    return