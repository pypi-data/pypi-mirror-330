import requests
import json
from common.exceptions import RemoteCallException
from ..env_config import env
from ..logging_config import logger

def get_upload_presigned_url(job_id, filename):
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN, "PositronJobId": job_id}
    url = f'{env.API_BASE}/generate-presigned-url?filename={filename}'
    logger.debug(f'Calling: {url}')
    response = requests.get(url, headers=Headers)
    logger.debug(response)
    if response.status_code != 200:
        raise RemoteCallException(f'Presigned url fetching failed with http code: {response.status_code} \n {response.text}')
    else:
        logger.debug(response.json())
        return response.json()
    
def get_download_presigned_url(job_id, filename):
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN, "PositronJobId": job_id}
    url = f'{env.API_BASE}/generate-download-url?filename={filename}'
    logger.debug(f'Calling: {url}')
    response = requests.get(url, headers=Headers)
    logger.debug(response)
    if response.status_code != 200:
        raise RemoteCallException(
            f'Presigned url fetching failed with http code: {response.status_code} \n {response.text}')
    else:
        logger.debug(response.json())
        return response.json()