from typing import Dict
import requests
import time
import typer
from common.env_config import env
from common.console import console
from common.exceptions import RemoteCallException, RobbieException

def get_device_code_payload():
    device_code_payload = {
        'client_id': env.AUTH0_CLIENT_ID,
        'scope': 'openid profile',
        'audience': env.AUTH0_AUDIENCE,
        'prompt': 'login'
    }
    device_code_response = requests.post(f'https://{env.AUTH0_DOMAIN}/oauth/device/code', data=device_code_payload)
    if device_code_response.status_code != 200:
        raise RobbieException(f'Error requesting device code: {device_code_response.text}')

    return device_code_response.json()

def get_user_auth_token(access_token: str) -> Dict[str, str]:
    auth_header = {
        'Authorization': f'Bearer {access_token}'
    }
    user_token_response = requests.get(f'{env.API_BASE}/get-user-auth-token', headers=auth_header)
    if user_token_response.status_code != 200:
        raise RemoteCallException.from_request(user_token_response)

    return user_token_response.json()

def wait_for_access_token(device_code_data):
    token_payload = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'device_code': device_code_data['device_code'],
        'client_id': env.AUTH0_CLIENT_ID
    }
    authenticated = False
    while not authenticated:
        console.print('Waiting for the user to login...')
        token_response = requests.post(f'https://{env.AUTH0_DOMAIN}/oauth/token', data=token_payload)

        token_data = token_response.json()
        if token_response.status_code == 200:
            console.print('Authenticated!')
            authenticated = True
            return token_data['access_token']
        elif token_data['error'] not in ('authorization_pending', 'slow_down'):
            print(token_data['error_description'])
            raise typer.Exit(code=1)
        else:
            time.sleep(device_code_data['interval'])
