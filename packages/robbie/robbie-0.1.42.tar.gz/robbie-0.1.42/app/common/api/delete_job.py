import requests
import json
from common.exceptions import RemoteCallException
from ..env_config import env
from ..logging_config import logger

def delete_job(job_id):
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN, "PositronJobId": job_id}
    url = f'{env.API_BASE}/delete-job'
    logger.debug(f'Calling: {url}')
    response = requests.post(url, headers=Headers, json=None)
    logger.debug(response)
    if response.status_code != 200:
        body = response.json()
        logger.debug(json.dumps(body, indent=2))
        if body.get('userFriendlyErrorMessage'):
            raise RemoteCallException(body.get('userFriendlyErrorMessage'))
        else:
            raise RemoteCallException(f'terminate_job failed with http code: {response.status_code} \n {response.text}')
    else:
        logger.debug(json.dumps(response.json(), indent=2))
        return response.json()