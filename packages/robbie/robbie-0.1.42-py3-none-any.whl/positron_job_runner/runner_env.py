import os
from dataclasses import dataclass
from dotenv import load_dotenv
from common.constants import RUNTIME_ENV_PREFIX
from typing import Union

load_dotenv()

# Disable stdout buffering
os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['POSITRON_CLOUD_ENVIRONMENT'] = '1'

@dataclass
class RunnerEnv():
  """
  The environment variables and other global vars required by the Runner.
  """
  USER_AUTH_TOKEN: str = os.getenv('USER_AUTH_TOKEN', "")
  SYSTEM_AUTHENTICATION_KEY: str = os.getenv('SYSTEM_AUTHENTICATION_KEY', "")
  REGION: str = os.getenv("REGION", "us-west-2")
  AWS_JOB_LOG_GROUP_NAME: str = os.getenv("AWS_JOB_LOG_GROUP_NAME", "")
  API_ENDPOINT: str = os.getenv("API_ENDPOINT", "")
  POSITRON_CLI_ENV: str = os.getenv("POSITRON_CLI_ENV", "development")
  POSITRON_CHARGE_INTERVAL: int = int(os.getenv('POSITRON_CHARGE_INTERVAL', 60))
  POSITRON_STDOUT_INTERVAL: int = int(os.getenv('POSITRON_STDOUT_INTERVAL', 2))
  POSITRON_CHECK_TERMINATION_INTERVAL: int = int(os.getenv('POSITRON_CHECK_TERMINATION_INTERVAL', 10))
  RUNNER_CWD: str = os.getenv('RUNNER_CWD')
  ROBBIE_CLI_PATH: str = os.getenv('ROBBIE_CLI_PATH', '$HOME/python-decorator')
  APP_NAME: str = os.getenv('APP_NAME', 'robbie')
  LOG_LEVEL: str = os.getenv('LOG_LEVEL', "DEBUG") # see logging.getLevelNameMapping()
  JOB_ID: Union[str, None] = os.getenv('JOB_ID', None)
  JOB_CWD: str = os.getenv('JOB_CWD')
  JOB_USER_CWD: str = os.getenv('JOB_USER_CWD')
  JOB_USER: Union[str, None] = os.getenv('JOB_USER', None)
  JOB_OWNER_EMAIL: Union[str, None] = os.getenv('JOB_OWNER_EMAIL', None)
  S3_BUCKET: str = os.getenv('S3_BUCKET', 'positron-dev-workspaces')
  AWS_ACCESS_KEY_ID: Union[str, None] = os.getenv('AWS_ACCESS_KEY_ID')
  AWS_SECRET_ACCESS_KEY: Union[str, None] = os.getenv('AWS_SECRET_ACCESS_KEY')
  REMOTE_FUNCTION_SECRET_KEY: str = os.getenv('REMOTE_FUNCTION_SECRET_KEY', "")
  rerun: bool = False

  def env_without_runner_env(self):
    """
    Will blacklist env vars we're explicitly expecting to be
    set by the infra and used by the Runner.
    """
    env = {}
    # if the var is prefixed, then it was passed by the user and should be included
    for k, v in os.environ.items():
      if k.startswith(RUNTIME_ENV_PREFIX):
        env[k[len(RUNTIME_ENV_PREFIX):]] = v

    # Manually set required vars.
    env['HOME'] = f"/home/{self.JOB_USER}"
    env['PWD'] = f"{self.JOB_USER_CWD}"
    env['PATH'] = f"/home/job_user/.conda/envs/robbie-runtime-env/bin:/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    env['PYTHONNOUSERSITE'] = '1'
    env['PYTHONUSERBASE'] = "/opt/conda"
    env['MAMBA_ROOT_PREFIX'] = f"{self.JOB_USER_CWD}/.mamba"
    # TODO: VIRTUAL_ENV to be deprecated:
    # env['VIRTUAL_ENV'] = f"{self.JOB_USER_CWD}/venv"
    env['PYTHONUNBUFFERED'] = '1'
    env['POSITRON_CLOUD_ENVIRONMENT'] = '1'

    # Explicitly set as this is just the users API key and will be used to calc integrity hash
    # in the subprocess if this is the remote function.
    env['REMOTE_FUNCTION_SECRET_KEY'] = self.REMOTE_FUNCTION_SECRET_KEY
    return env

runner_env = RunnerEnv()
