import inspect

from keeshond import logging_logger

log = logging_logger.getlogger(__name__, logging_logger.DEBUG)


def analyze(_object):
    # Get the current frame
    log.debug(f"{inspect.currentframe().f_back.f_locals=}")
    log.debug(f"{type(_object)=}")
    log.debug(f"{dir(_object)=}")
    try:
        log.debug(f"{_object.__dict__=}")
    except Exception as e:
        log.warning(f"_object.__dict__ {e=}")
    try:
        log.debug(f"{vars(_object)=}")
    except Exception as e:
        log.warning(f"vars(_object) {e=}")
    log.debug(f"{help(_object)=}")
    try:
        log.debug(f"{inspect.getargvalues(_object)=}")
    except Exception as e:
        log.warning(f"inspect.getargvalues(_object) {e=}")
        pass
    log.debug(f"{inspect.getmembers(_object)=}")
