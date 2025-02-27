import logging
import sys

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


def getlogger(_name, _level=logging.ERROR):
    """python
    from keeshond import logging_logger
    log = logging_logger.getlogger(__name__)
    """

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logger = logging.getLogger(_name)
    logger.setLevel(_level)
    if not logger.hasHandlers():
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - "%(pathname)s:%(lineno)d" - %(funcName)s:  %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.info(f"{logger.name=} with level {logging.getLevelName(logger.getEffectiveLevel())} is enabled")
    return logger
