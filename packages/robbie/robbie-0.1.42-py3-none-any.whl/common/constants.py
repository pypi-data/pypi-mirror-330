import os

APP_NAME = "robbie"
APP_HOME_DIR = os.path.expanduser("~/.robbie")
JOB_CONF_YAML_PATH = "./job_config.yaml"

NERC_CLUSTER = "NERC"
EKS_CLUSTER = "EKS"

# Used to prefix environment variables that are passed to the runtime environment
RUNTIME_ENV_PREFIX: str = '__RUNTIME_'

# 50MB
FILE_SIZE_THRESHOLD = 50 * 1024 * 1024
