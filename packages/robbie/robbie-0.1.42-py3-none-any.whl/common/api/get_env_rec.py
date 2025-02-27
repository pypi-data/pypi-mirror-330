import requests
import json
import pprint
import re
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from common.utils import undefined
from common.config import PositronJob
from common.cli_args import args as cli_args
from common.env_config import env
from common.exceptions import RemoteCallException, RobbieException
from common.logging_config import logger
from common.env_defaults import current

class GetEnvRecBody(BaseModel):
    """
    Maps to the request body of the Create Job API
    """
    model: Optional[str] = Field(default=undefined)
    prompt: List[List[str]] = Field(default=undefined)

    def http_dict(self) -> Dict[str, Any]:
        """
        Enables dropping fields that were never set and should be treated as undefined
        """
        return {k: v for k, v in self.__dict__.items() if v is not undefined}

def get_env_rec( 
    system_prompt: str,
    human_prompt: str,
    model: str = None
) -> str:
    """
        Use GenAI to get an environment recommendation

        Args:
            python_code (str): The python code to be run

        Returns:
            str: The environment_id recommendation
    """
    prompt = [["system", system_prompt], ["human", human_prompt]]

    if model is None:
        data = GetEnvRecBody(
            prompt=prompt
        )
    else: 
        data = GetEnvRecBody(
            model=model,
            prompt=prompt
        )
    # print(pprint.pformat(data.http_dict()))

    
    url = f'{env.API_BASE}/get-env-rec'
    logger.debug(f'Calling: {url}')
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN}
    response = requests.post(url, headers=Headers, json=data.http_dict())
    logger.debug(response)
    if response.status_code != 200:
        body = response.json()
        logger.debug(json.dumps(body, indent=2))
        # TODO: need standard error codes in errors
        if body.get('userFriendlyErrorMessage'):
            raise RemoteCallException(body.get('userFriendlyErrorMessage'))
        else:
            raise RemoteCallException(f'get_env_rec() failed with http code: {response.status_code} \n {response.text}')
    else:
        # logger.debug(response.json())
        logger.debug(json.dumps(response.json(), indent=2))
        return response.json()
