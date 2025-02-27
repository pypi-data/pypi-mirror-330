import requests
import json
from common.exceptions import RemoteCallException
from ..env_config import env
from ..logging_config import logger

def get_pd_auth():
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN }
    url = f'{env.API_BASE}/get-pd-auth' 
    
    logger.debug(f'Calling: {url}')
    response = requests.get(url, headers=Headers)
    
    logger.debug(response)
    if response.status_code != 200:
        body = response.json()
        logger.debug(json.dumps(body, indent=2))
        if body.get('userFriendlyErrorMessage'):
            raise RemoteCallException(body.get('userFriendlyErrorMessage'))
        else:
            raise RemoteCallException(f'get_pd_auth: {response.status_code} \n {response.text}')
    else:
        logger.debug(json.dumps(response.json(), indent=2))
        return response.json()