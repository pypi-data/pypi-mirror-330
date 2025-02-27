import yaml
from typing import Optional
from pydantic import BaseModel
import os
from common.constants import APP_HOME_DIR
from common.logging_config import logger
from common.console import console, print_boxed_messages

DEFAULT_USER_CONFIG_PATH = f"{APP_HOME_DIR}/config.yaml"

class UserConfigFile(BaseModel):
    """
    The user configuration file for the Robbie CLI.
    """
    user_auth_token: Optional[str] = None
    backend_api_base_url: Optional[str] = None
    backend_ws_base_url: Optional[str] = None
    sentry_dsn: Optional[str] = None
    
    def load_config(self):
        """
        Loads the user configuration from the user's home directory.
        """
        if not os.path.exists(DEFAULT_USER_CONFIG_PATH):
            logger.debug(f'user config file not found: `{DEFAULT_USER_CONFIG_PATH}`')
            return

        try:
            with open(DEFAULT_USER_CONFIG_PATH, 'r') as user_config_file:
                user_config_dict = yaml.safe_load(user_config_file)
                self.__dict__.update(**user_config_dict)
        except Exception as e:
            console.print(f'[red]Error loading user configuration! {str(e)}[/red]')
            console.print(f'[yellow]Ignoring user config file: `{DEFAULT_USER_CONFIG_PATH}`[/yellow]')
    
    def write(self):
        """
        Write the user configuration to the user's home directory.
        """
        data = self.model_dump(exclude_none=True)
        os.makedirs(os.path.dirname(DEFAULT_USER_CONFIG_PATH), exist_ok=True)
        with open(DEFAULT_USER_CONFIG_PATH, 'w') as user_config_file:
            yaml.dump(data, user_config_file)
    
    def to_string(self, include_title: bool = False) -> str:
        """
        Print the user configuration to the console.
        """
        message = f"""- User Auth Token: {self.user_auth_token}
- Backend API Base URL: {self.backend_api_base_url}
- Backend WS Base URL: {self.backend_ws_base_url}"""
        if include_title:
            return f"========== User Config (user_config) ==========\n{message}"
        else:
            return message
 

user_config = UserConfigFile()
"""
The user configuration file for the Robbie CLI.
"""

if os.getenv('POSITRON_CLOUD_ENVIRONMENT'):
    logger.debug("Cloud environment detected, skipping config file load.")
else:
    logger.debug('loading user config')
    user_config.load_config()
