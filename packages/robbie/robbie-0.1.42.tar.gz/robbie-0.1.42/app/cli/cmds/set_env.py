import typer
from typing_extensions import Annotated
from common.observability.main import track_command_usage
from common.user_config import user_config
from common.env_defaults import env_config, EnvType
from common.console import console
from cli.auto_complete import set_env_auto_complete

@track_command_usage("set_env")
def set_env(
  env: Annotated[str, typer.Argument(autocompletion=set_env_auto_complete)] = 'dev',
):
    current = env_config[EnvType(env)]
    user_config.backend_api_base_url = current.api_base
    user_config.backend_ws_base_url = current.ws_base
    user_config.write()
    console.print(f'Successfully updated config.')
    console.print(f'[bold]Env[/bold]: {env}')
    console.print(f'[bold]API[/bold]: {current.api_base}')
    console.print(f'[bold]WS [/bold]: {current.ws_base}')
