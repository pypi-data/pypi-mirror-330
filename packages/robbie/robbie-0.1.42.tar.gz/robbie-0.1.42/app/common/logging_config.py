import json
import logging
import time
import os
from logging import _nameToLevel
from typing import Optional
from .console import console
from functools import wraps

APP_NAME = "robbie.cli"
LOG_LEVEL = os.getenv("ROBBIE_LOG_LEVEL", "ERROR").upper()
JSON_LOGS=False
JSON_LOGS_PRETTY=False
JSON_LOGS_INCLUDE_SRC_LINE=False

log_level = _nameToLevel.get(LOG_LEVEL, 20)

class _UTCFormatter(logging.Formatter):
    """Class that overrides the default local time provider to GMT in log formatter."""
    converter = time.gmtime


    def format(self, record):
        if not JSON_LOGS:
            return super(_UTCFormatter, self).format(record)

        log_record = {
            "asctime": time.strftime("%Y-%m-%d %H:%M:%S:%MS", self.converter(record.created)),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
        }

        if JSON_LOGS_INCLUDE_SRC_LINE:
            relative_path = os.path.relpath(record.pathname)
            # Append the line number to the relative path
            relative_path_with_lineno = f"{relative_path}:{record.lineno}"
            log_record["pathname"] = relative_path_with_lineno

        if JSON_LOGS_PRETTY:
            return json.dumps(log_record, indent=4)
        return json.dumps(log_record)

logger = logging.getLogger(APP_NAME)

logger.setLevel(log_level)
handler = logging.StreamHandler()
formatter = _UTCFormatter("%(asctime)s %(name)s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def set_log_level(loglevel: Optional[str]):
    if loglevel is None:
        return
    level_int = _nameToLevel.get(loglevel)
    if level_int is None:
        console.print("[red]Invalid log level")
        return
    logger.setLevel(level_int)
    console.print("[green]loglevel set to: ", loglevel)

# TODO: Not sure if we really need this.
# don't stream logs with the root logger handler
logger.propagate = 0

# this is fake so things will compile
"""
def logger_module(module):
    def _logger_module(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result
        return wrapper
    return _logger_module
"""

if __name__ == "__main__":
    """Testing"""
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")