import webbrowser
import typer
from typing_extensions import Annotated
from common.user_config import user_config, DEFAULT_USER_CONFIG_PATH   
from common.logging_config import logger
from common.console import console
from common.constants import APP_NAME, APP_HOME_DIR
from common.api.login import get_device_code_payload, get_user_auth_token, wait_for_access_token
from common.api.validate_user_auth_token import is_auth_token_valid
from common.api.get_pd_auth import get_pd_auth
from common.env_config import env
from common.exceptions import RemoteCallException
from common.observability.main import track_command_usage


@track_command_usage("login")
def login(
    ctx: typer.Context = None,
    force: Annotated[bool, typer.Option("--force", help='Force the creation of a new API key')] = False,
) -> None:
    """
    Logs you in to your Robbie account and stores API key on your local machine.
    """
    if force or (not user_config.user_auth_token or not is_auth_token_valid()):
        # Get device code
        try:
            if not force:
                console.print('[red]Your Robbie API key is not valid, logging in.[/red]')

            console.print('Authenticating with Robbie...')
            device_code_data = get_device_code_payload()

            # Redirect to login
            console.print("1. If a browser window doesn't automatically launch, navigate to: ", device_code_data['verification_uri_complete'])
            console.print('2. Confirm the following code: ', device_code_data['user_code'])
            console.print('3. Enter your username and password!')
            console.print('')
            webbrowser.open(url=device_code_data['verification_uri_complete'], new=2, autoraise=True)

            # Wait for authentication
            access_token = wait_for_access_token(device_code_data)
            logger.debug(f'Access Token: {access_token}')

            # console.print('Requesting User Auth Token')
            user_token_response_data = get_user_auth_token(access_token)

            console.print(f'[green]Writing {APP_NAME} API key to: {DEFAULT_USER_CONFIG_PATH}')
            save_user_token(
                user_token_response_data['userAuthToken'],
                user_token_response_data['sentryDsn']
            )
            # ensure that "env" is updated with the new user token if it was imported previsouly
            env.USER_AUTH_TOKEN = user_config.user_auth_token

            # call this to make certain we have the identity pool created for PD functions
            logger.debug('Getting PD Auth') 
            result = get_pd_auth()
            logger.debug(f"Retrieved Identity ID: {result['identityId']}")

        except RemoteCallException as e:
            logger.debug(e, exc_info=True)
            console.print(f"[red]{e.user_friendly_message}")
            raise typer.Exit(code=1)
        except Exception as e:
            logger.debug(e, exc_info=True)
            console.print(f"[red]An error occurred: {e}. If the problem continues, reach out to our support team for help.\nEmail: support@robbie.run[/red]")
            raise typer.Exit(code=1)
    else:
        # was the command invoked from the CLI 
        if ctx:
            console.print(f'[green]You are good to go![/green]')
        

def save_user_token(user_token, sentry_dsn):
    user_config.user_auth_token = user_token
    user_config.sentry_dsn = sentry_dsn
    user_config.write()
    
