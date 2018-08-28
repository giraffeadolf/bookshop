import logging
import logging.handlers

logger = logging.getLogger("test_log")
fn = logging.FileHandler("log.log")
fn.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s ")
fn.setFormatter(formatter)
logger.addHandler(fn)
logger.setLevel(logging.DEBUG)


def log(message):
    def wrap(func):
        logger.info(message)
        result = func
        return result
    return wrap