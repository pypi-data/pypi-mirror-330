from typing import Dict
from dataclasses import dataclass
from .build_env import build_env, EnvType
from common.logging_config import logger
from common.console import console, print_boxed_messages

@dataclass
class EnvDefaults():
  name: str
  portal_base: str
  api_base: str
  ws_base: str
  auth0_domain: str
  auth0_audience: str
  auth0_client_id: str

  def to_string(self, include_title: bool = False) -> str:
    message = f"""- EnvDefaults: {self.name}
- portal_base: {self.portal_base}
- api_base: {self.api_base}
- ws_base: {self.ws_base}
- auth0_domain: {self.auth0_domain}
- auth0_audience: {self.auth0_audience}
- auth0_client_id: {self.auth0_client_id}"""
    if include_title:
      return f"========== EnvDefaults ==========\n{message}"
    else:
      return message

    

env_config: Dict[EnvType, EnvDefaults] = {
  EnvType.LOCAL: EnvDefaults(
    name='local',
    portal_base='http://localhost:3000',
    api_base='http://localhost:3002/api',
    ws_base='ws://localhost:3002',
    auth0_domain='dev-k1t01pbanrr04itm.us.auth0.com',
    auth0_client_id='Mr3GW8Ub4e2bLaEvZ5o0XK5pGfEhtH3d',
    auth0_audience='https://localhost/positron/api',
  ),
  EnvType.DEV: EnvDefaults(
    name='dev',
    portal_base='https://dev.positronsupercompute.com',
    api_base='https://dev.positronsupercompute.com/api',
    ws_base='wss://dev.positronsupercompute.com',
    auth0_domain='dev-k1t01pbanrr04itm.us.auth0.com',
    auth0_client_id='Mr3GW8Ub4e2bLaEvZ5o0XK5pGfEhtH3d',
    auth0_audience='https://localhost/positron/api',
  ),
  EnvType.ALPHA: EnvDefaults(
    name='alpha',
    portal_base='https://alpha.positronsupercompute.com',
    api_base='https://alpha.positronsupercompute.com/api',
    ws_base='wss://alpha.positronsupercompute.com',
    auth0_domain='dev-k1t01pbanrr04itm.us.auth0.com',
    auth0_client_id='Mr3GW8Ub4e2bLaEvZ5o0XK5pGfEhtH3d',
    auth0_audience='https://localhost/positron/api',
  ),
  EnvType.BETA: EnvDefaults(
    name='beta',
    portal_base='https://robbie.run',
    api_base='https://robbie.run/api',
    ws_base='wss://robbie.run',
    auth0_domain='login.robbie.run',
    auth0_client_id='ZW0vio95rYfbHrN7kE3PoUXwmPloBw7e',
    auth0_audience='https://beta/positron/api',
  ),
}



current = env_config[EnvType.DEV]
# current = env_config[EnvType.LOCAL]

# Set current based on build
if build_env:
  current = env_config[build_env]
  logger.debug(f'Using build environment: "{build_env.value}" backend url: "{current.api_base}"')
