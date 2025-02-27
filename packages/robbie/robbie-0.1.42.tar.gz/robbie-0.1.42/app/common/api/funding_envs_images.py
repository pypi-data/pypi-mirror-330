import requests
import json
from ..exceptions import RemoteCallException
from ..env_config import env
from ..logging_config import logger

# keys
FS_ID="id"
FS_NAME="name"
FS_TOKENS="userTokens"
FS_MENU="menu"
FS_TYPE="type"
FS_DEFAULT_IMAGE_NAME="defaultImageName"
FS_DEFAULT_IMAGE_ID="defaultImageId"
FS_DEF_ENV_NAME="defaultEnvironmentName"
FS_DEF_ENV_ID="defaultEnvironmentId"
FS_PERSONAL_NAME="Personal"
FS_PERSONAL_TYPE="PERSONAL"

# API call
def list_funding_sources():
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN  }
    url = f'{env.API_BASE}/list-funding-sources'
    logger.debug(f'list_funding_sources Calling: {url}')
    response = requests.get(url, headers=Headers)
    logger.debug(response)
    if response.status_code != 200:
        body = response.json()
        logger.debug(json.dumps(body, indent=2))
        if body.get('userFriendlyErrorMessage'):
            raise RemoteCallException(body.get('userFriendlyErrorMessage'))
        else:
            raise RemoteCallException(f'list_funding_sources failed with http code: {response.status_code} \n {response.text}')
    else:
        logger.debug(json.dumps(response.json(), indent=2))
        return response.json()
    
# keys
ENV_NAME="name"
# note there is a duplicate "environmentName" key in the API response that points to the same thing
ENV_ID="id"
ENV_TPH="tokensPerHour"
ENV_MENU_ITEM="menu"
ENV_CLUSTER_TYPE="clusterType"
ENV_DESCRIPTION="description"
ENV_GPU_NUMBER="gpuNumber"
ENV_DELETED="deleted"
ENV_ENVNAME="environmentName"
ENV_CPU="cpu"
ENV_RAM="ram"
ENV_DISK="disk"
ENV_GPU_TYPE="gpuType"
ENV_NODE_TYPE="nodeType"


# API call
def list_environments(fs_id: str):
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN, "fundingGroupId": fs_id  }
    url = f'{env.API_BASE}/list-environments'
    logger.debug(f'Calling: {url}')
    response = requests.get(url, headers=Headers)
    logger.debug(response)
    if response.status_code != 200:
        body = response.json()
        logger.debug(json.dumps(body, indent=2))
        if body.get('userFriendlyErrorMessage'):
            raise RemoteCallException(body.get('userFriendlyErrorMessage'))
        else:
            raise RemoteCallException(f'list_environments failed with http code: {response.status_code} \n {response.text}')
    else:
        logger.debug(json.dumps(response.json(), indent=2))
        return response.json()

# keys  
IMAGE_NAME="imageName"
IMAGE_ID="id"
IMAGE_MENU_ITEM="menu"
IMAGE_DELETED="deleted"

# API call
def list_images(fs_id: str, env_id: str):
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN, "fundingGroupId": fs_id, "environmentId": env_id  }
    url = f'{env.API_BASE}/list-images'
    logger.debug(f'Calling: {url}')
    response = requests.get(url, headers=Headers)
    logger.debug(response)
    if response.status_code != 200:
        body = response.json()
        logger.debug(json.dumps(body, indent=2))
        if body.get('userFriendlyErrorMessage'):
            raise RemoteCallException(body.get('userFriendlyErrorMessage'))
        else:
            raise RemoteCallException(f'list_images failed with http code: {response.status_code} \n {response.text}')
    else:
        logger.debug(json.dumps(response.json(), indent=2))
        return response.json()
