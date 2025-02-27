import requests
import json
import pprint
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from common.utils import undefined
from common.config import PositronJob
from common.cli_args import args as cli_args
from common.env_config import env
from common.exceptions import RemoteCallException, RobbieException
from common.logging_config import logger
from common.env_defaults import current

class CreateJobBody(BaseModel):
    """
    Maps to the request body of the Create Job API
    """
    userDefinedName: Optional[str] = Field(default=undefined)
    fundingGroupId: Optional[str] = Field(default=undefined)
    imageName: Optional[str] = Field(default=undefined)
    environmentId: Optional[str] = Field(default=undefined)
    jobArguments: Optional[List[str]] = Field(default=undefined)
    entryPoint: Optional[str] = Field(default=undefined)
    commands: Optional[str] = Field(default=undefined)
    maxTokens: Optional[int] = Field(default=undefined)
    maxMinutes: Optional[int] = Field(default=undefined)

    def http_dict(self) -> Dict[str, Any]:
        """
        Enables dropping fields that were never set and should be treated as undefined
        """
        return {k: v for k, v in self.__dict__.items() if v is not undefined}

    @staticmethod
    def from_config(job_config: PositronJob):
        instance = CreateJobBody(
            maxTokens=job_config.max_tokens,
            maxMinutes=job_config.max_time,
        )
        if not job_config.job_type:
            raise RobbieException("Internal error: Job type is not set")
        instance.entryPoint = job_config.job_type.value
        if job_config.name:
            instance.userDefinedName = job_config.name
        if job_config.commands:
            instance.commands = ";\n".join(job_config.commands)
        if cli_args.job_args:
            instance.jobArguments = cli_args.job_args
        else:
            instance.jobArguments = []
        if job_config.funding_group_id:
            instance.fundingGroupId = job_config.funding_group_id
        if job_config.image:
            instance.imageName = job_config.image
        if job_config.environment_id:
            instance.environmentId = job_config.environment_id
        return instance



def create_job(job_config: PositronJob):
    data = CreateJobBody.from_config(job_config)
    logger.debug(pprint.pformat(data.http_dict()))
    url = f'{env.API_BASE}/create-job'
    logger.debug(f'Calling: {url}')
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN}
    response = requests.post(url, headers=Headers, json=data.http_dict())
    logger.debug(response)
    if response.status_code != 200:
        body = response.json()
        logger.debug(json.dumps(body, indent=2))
        # TODO: need standard error codes in errors
        if (body.get('message').lower() == 'concurrent job limit exceeded'):
            additional_help = [
                "You can free up capacity by terminating running jobs or reaching out to your group's",
                "administrator to increase your concurrent job limit.",
                f"{current.portal_base}/portal/app/my-runs"
            ]
            raise RemoteCallException(
                reason=body.get('message').lower(),
                user_friendly_message=body.get('userFriendlyErrorMessage'),
                additional_help="\n".join(additional_help)
            )
        if body.get('userFriendlyErrorMessage'):
            raise RemoteCallException(body.get('userFriendlyErrorMessage'))
        else:
            raise RemoteCallException(f'Job creation failed with http code: {response.status_code} \n {response.text}')
    else:
        # logger.debug(response.json())
        logger.debug(json.dumps(response.json(), indent=2))
        return response.json()

