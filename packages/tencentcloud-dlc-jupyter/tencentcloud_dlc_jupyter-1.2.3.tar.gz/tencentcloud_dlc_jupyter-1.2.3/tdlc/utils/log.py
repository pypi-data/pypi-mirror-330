from . import constants

from tdlc.utils import configurations

import sys
import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "defaultFormatter": {
            "format": "[%(asctime)s][%(levelname)s]%(message)s",
            'datefmt': "",
        }
    },
    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "formatter": "defaultFormatter",
            "stream": sys.stdout,
        },
        "fileHandler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "defaultFormatter",
            "maxBytes": 1024*1024*64,
            "backupCount": 5,
            "filename": configurations.LOG_FILE.get()
        },
    },
    "loggers": {
        "default": {
            "handlers": ["fileHandler"],
            "level": configurations.LOG_LEVEL.get()
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

def getLogger(name):
    return _LoggerWrapper(name)


class _LoggerWrapper():

    def __init__(self, module) -> None:
        self._module = module
        self._logger = logging.getLogger('default')
    
    def _attach_with_module(self, msg):
        return f'[{self._module}] {msg}'

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(self._attach_with_module(msg), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._logger.info(self._attach_with_module(msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(self._attach_with_module(msg), *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(self._attach_with_module(msg), *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._logger.critical(self._attach_with_module(msg), *args, **kwargs)



