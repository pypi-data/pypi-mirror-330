from common.utils import get_version
from common.build_env import build_env
from common.env_defaults import current
from common.console import console
from common.observability.main import track_command_usage

@track_command_usage("version")
def version():
    console.print(f"Robbie SDK Version: {get_version()}, build_env: {build_env.value}, current_env: {current.name}")
