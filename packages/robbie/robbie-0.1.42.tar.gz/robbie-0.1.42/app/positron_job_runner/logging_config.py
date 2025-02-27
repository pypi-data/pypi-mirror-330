import json
import logging
import time
import os
from .runner_env import runner_env
from logging import _nameToLevel

LOGGER_NAME = f"{runner_env.APP_NAME}.job_runner"
JSON_LOGS=False
JSON_LOGS_PRETTY=False
JSON_LOGS_FILE_PATH=False

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

        if JSON_LOGS_FILE_PATH:
            relative_path = os.path.relpath(record.pathname)
            # Append the line number to the relative path
            relative_path_with_lineno = f"{relative_path}:{record.lineno}"
            log_record["pathname"] = relative_path_with_lineno

        if JSON_LOGS_PRETTY:
            return json.dumps(log_record, indent=4)
        return json.dumps(log_record)

def get_logger():
    logger = logging.getLogger(LOGGER_NAME)
    if len(logger.handlers) == 0:
        logger.setLevel(_nameToLevel.get(runner_env.LOG_LEVEL))
        handler = logging.StreamHandler()
        formatter = _UTCFormatter("%(asctime)s %(name)s %(levelname)-8s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # don't stream logs with the root logger handler
        logger.propagate = 0

    return logger
