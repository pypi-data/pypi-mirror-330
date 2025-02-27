from pydantic import BaseModel, SerializeAsAny, field_validator
from typing import Dict, Optional, List, Union
import os
import copy
import yaml
import re
from yaml import dump
from enum import Enum
from common.utils import get_version, _valid_python_versions
from common.exceptions import RobbieException
from common.user_config import user_config
from common.constants import JOB_CONF_YAML_PATH, RUNTIME_ENV_PREFIX
from common.logging_config import logger
from common.enums import JobRunType
from positron_job_runner.runtime_environment_manager import (
    CONDA_MODE,
    PYTHON_MODE,
    GENERIC_MODE,
    _running_in_conda
)
from common.console import console
from common.image_name import get_auto_image_name_and_cluster
from common.api.funding_envs_images import *

backward_comptability_1_0 = False

class PositronJob(BaseModel):
    """
    The Job details as defined in the `python_job` from the `job_config.yaml` file.
    """
    name: Optional[str] = None
    job_type: Optional[JobRunType] = None
    mode: Optional[str] = None
    rpv: Optional[str] = None # only set if we change the python version
    funding_group_id: Optional[str] = None
    environment_id: Optional[str] = None
    cluster: Optional[str] = None
    image: Optional[str] = None # this is not written to the config file
    workspace_dir: Optional[str] = None # deprecated
    include_local_dir: Optional[bool] = False
    custom_file_filter: Optional[List[str]] = None
    dependencies: Optional[str] = None
    max_tokens: Optional[int] = None
    max_time: Optional[int] = None
    env: Optional[Dict[str, str]] = None
    commands: Optional[List[str]] = None
    # below are values not written to the config file
    filename: Optional[str] = None
    robbie_sdk_version: Optional[str] = get_version()
    image_selection: Optional[str] = None
    funding_selection: Optional[str] = None
    environment_selection: Optional[str] = None
    rpv_selection: Optional[str] = None
    dep_selection: Optional[str] = None
    name_selection: Optional[str] = None
    include_local_dir_selection: Optional[str] = None
    mode_selection: Optional[str] = None
    verbose: Optional[bool] = False
        
    # remote python version
    @field_validator('rpv', mode='after')
    def ensure_valid_python_version(cls, rpv):
        rpv_list = _valid_python_versions()
        rpv_list.append("local")
        if rpv in rpv_list:
            return rpv
        else:
            raise ValueError('Invalid Python version, must be "3.9", "3.10, "3.11", or "3.12"')
        
    @field_validator('dependencies', mode='after')
    def ensure_valid_dependies(cls, dependencies):
        if (dependencies == "auto-capture" or
            dependencies == "none" or 
            dependencies.endswith(".txt") or 
            dependencies.endswith(".yml") or 
            dependencies.endswith(".yaml")):
            return dependencies
        else:
            raise ValueError('Invalid dependencies. Must be "auto-capture", "none", or end with ".txt", ".yml", or ".yaml"')
        
    @field_validator('commands', mode='after')
    def ensure_non_empty(cls, commands):
        return commands if len(commands) else None

    @field_validator('env', mode='after')
    def ensure_env_is_dict(cls, v):
        if isinstance(v, dict):
            return v
        raise ValueError('env must be a dictionary')

    @field_validator('workspace_dir', mode='after')
    def workspace_dir_deprecation_warning(cls, workspace_dir):
        console.print("[yellow] Warning: workspace_dir is deprecated. Please use include_local_dir instead.")
        return workspace_dir
    
    @field_validator('max_time', mode='before')
    def ensure_max_time_is_int(cls, max_time: Union[int, str, None]) -> Union[int, None]:
        return cls._max_time_to_minutes(max_time)

    @field_validator('max_tokens', mode='before')
    def ensure_max_tokens_is_int(cls, max_tokens: Union[int, str, None]) -> Union[int, None]:
        return cls._max_tokens_to_int(max_tokens)

    def create_runtime_env(self) -> Dict[str, str]:
        """
        Used on the client side to create the prefixed runtime environment variables
        to avoid conflicts with the local environment variables.
        """
        env: Dict[str, str] = {}
        # cycle through the env vars and prefix them
        if not self.env:
            return env
        for key, value in self.env.items():
            if (value == ""):
                env_var = os.environ.get(key)
                if env_var is None:
                    raise ValueError(f"The env prop {key} is unset inside job_config.yaml and also unset in local env vars. Please set this value.")
                env[f'{RUNTIME_ENV_PREFIX}{key}'] = env_var
            else:
                env[f'{RUNTIME_ENV_PREFIX}{key}'] = value
        return env

    @staticmethod
    def _max_time_to_minutes(max_time: Union[int, str, None]) -> Union[int, None]:
        if not max_time:
            return None
        if isinstance(max_time, int):
            return max_time
        matches = re.search(r'^(\d+):(\d{2})$', max_time)
        if matches is None:
            raise ValueError(f'Invalid Job Config: Field "max_time" ({max_time}) must have the format "HH:MM" or be a positive integer')
        try:
            hours = int(matches.group(1))
            minutes = int(matches.group(2))
        except:
            raise ValueError(f'Invalid Job Config: Field "max_time" ({max_time}) must have the format "HH:MM" or be a positive integer')
        if minutes >= 60:
            raise ValueError('Invalid Job Config: Field "max_time" ({max_time}) has invalid minutes! Must be 0 <= minutes < 60!')
        return hours * 60 + minutes

    @staticmethod
    def _max_tokens_to_int(max_tokens: Union[int, str, None]) -> Union[int, None]:
        if not max_tokens:
            return None
        if isinstance(max_tokens, int):
            return max_tokens
        try:
            max_tokens = int(max_tokens)
        except:
            raise ValueError(f'Invalid Job Config: "max_tokens" ({max_tokens}) needs to be a positive integer.')
        if max_tokens <= 0:
            raise ValueError(f'Invalid Job Config: "max_tokens" ({max_tokens}) needs to be a positive integer.')
        return max_tokens

    def validate_values(self) -> None:
        errors = []
        if self.env and not validate_env_vars(self.env):
            errors.append('At least one of the environment variables provided is invalid')
        if errors:
            raise RobbieException(f'Invalid configuration. Errors: {errors}')
        return None
    
    def namestr(self, obj, namespace):
        return [name for name in namespace if namespace[name] is obj]

    def to_string(self, title: str = None):
        message = f"""
- filename: {self.filename}
- name: {self.name}
    - name_selection: {self.name_selection}
- job_type: {self.job_type}
- mode: {self.mode}
    - mode_selection: {self.mode_selection}
- rpv: {self.rpv}
    - rpv_selection: {self.rpv_selection}
- robbie_sdk_version: {self.robbie_sdk_version}
- funding_group_id: {self.funding_group_id}
    - funding_selection: {self.funding_selection}
- environment_id: {self.environment_id}
    - environment_selection: {self.environment_selection}
- image: {self.image}
    - image_selection: {self.image_selection}
- cluster: {self.cluster}
- dependencies: {self.dependencies}
    - dep_selection: {self.dep_selection}
- custome_file_filter: {self.custom_file_filter}
- verbose: {self.verbose}
- workspace_dir: {self.workspace_dir}
- include_local_dir: {self.include_local_dir}
    - include_local_dir_selection: {self.include_local_dir_selection}
- max_tokens: {self.max_tokens}
- max_time: {self.max_time}
- env: {self.env}
- commands: {self.commands}"""

        if title:
            return f"========== {title} ==========\n{message}"
        else:
            return message
        
    def deepcopy(self):
        return copy.deepcopy(self)
        

class PositronJobConfig(BaseModel):
    """
    The `job_config.yaml` schema class.
    """
    version: float
    python_job: PositronJob

    def write_to_file(this, filename: str = JOB_CONF_YAML_PATH):
        copy_of_config = copy.deepcopy(this)
        if copy_of_config.python_job.rpv == "local":
            del copy_of_config.python_job.rpv
        del copy_of_config.python_job.robbie_sdk_version
        del copy_of_config.python_job.cluster
        del copy_of_config.python_job.image_selection
        del copy_of_config.python_job.funding_selection
        del copy_of_config.python_job.environment_selection
        del copy_of_config.python_job.rpv_selection
        del copy_of_config.python_job.dep_selection
        del copy_of_config.python_job.name_selection
        del copy_of_config.python_job.include_local_dir_selection
        del copy_of_config.python_job.mode_selection
        del copy_of_config.python_job.verbose
        del copy_of_config.python_job.filename

        config_dict = copy_of_config.model_dump(
            exclude_unset=True,
        )
        config_dict = convert_enums_to_values(config_dict)

        with open(filename, 'w') as file:
            file.write(dump(config_dict, sort_keys=False))


def convert_enums_to_values(d: dict) -> dict:
    """
    Converts Enum type values in the dictionary to their respective values.
    """
    for key, value in d.items():
        if isinstance(value, Enum):
            d[key] = value.value
        elif isinstance(value, dict):
            convert_enums_to_values(value)
    return d

def convert_enums_to_values(d: dict) -> dict:
    """
    Converts Enum type values in the dictionary to their respective values.
    """
    for key, value in d.items():
        if isinstance(value, Enum):
            d[key] = value.value
        elif isinstance(value, dict):
            convert_enums_to_values(value)
    return d

def is_valid_key_value(keyvalue):
    """
    Validate that the key-value contains only alphanumeric characters, dashes, and underscores, and has no spaces.
    """
    return bool(re.match(r'^[\w-]+$', keyvalue))

def validate_env_vars(env_dict):
    """
    Validate the environment variables from the given dictionary.
    """
    valid = True
    for key, value in env_dict.items():
        if not is_valid_key_value(key):
            print(f"Invalid key (contains invalid characters or spaces): {key}")
            valid = False
        if value != "" and not is_valid_key_value(value):
            print(f"Invalid value (contains invalid characters or spaces): {value}")
            valid = False
    return valid

def merge_config(base_config: PositronJob, override_config: PositronJob) -> PositronJob:
    """
    Makes it easy to merge decorator configs on top of the YAML config.
    """
    update_data = override_config.model_dump(exclude_unset=True)
    updated_config = base_config.model_copy(update=update_data)
    return updated_config


def invalid_yaml_keys(yaml_job_keys) -> bool:
    """
    Validates the yaml keys against the PositronJob class.
    """
    # Get only attributes from PositronJob
    base_attrs = set(dir(BaseModel))
    derived_attrs = set(dir(PositronJob()))
    additional_attrs = derived_attrs - base_attrs

    # Exclude built-in attributes (e.g., __init__, __module__)
    validKeys = [attr for attr in additional_attrs if not attr.startswith('__')]
    
    weHaveInvalidYamlKeys = False
    for key in yaml_job_keys:
        if key not in validKeys:
            weHaveInvalidYamlKeys = True
            raise RobbieException(f'Error: wrong param in the job_config.yaml: -> {key}')

    return weHaveInvalidYamlKeys

def load_job_config(config_path: str = './job_config.yaml') -> Optional[PositronJob]:
    """
    Load the job configuration from the `job_config.yaml` file if it exists
    """
    if not os.path.exists(config_path):
        logger.debug(f'{config_path} file not found')
        return None
    
    try:
        # this happens sometimes and it causes the job to fail
        if os.path.getsize(config_path) == 0:
            logger.debug(f'{config_path} file is empty')
            return None
        with open(config_path, 'r') as job_config_file:
            job_config_dict = yaml.safe_load(job_config_file)
            job = job_config_dict["python_job"]
            if invalid_yaml_keys(job.keys()):
                return None
            job_config = PositronJobConfig(**job_config_dict)

            logger.debug(f"job_config.version: {job_config.version}")
            if job_config:
                job_config.python_job.filename = config_path
                if job_config.version == 1.0:
                    global backward_comptability_1_0
                    backward_comptability_1_0 = True

                    console.print(f"[bold yellow]Warning: Your job_config.yaml file is using an older version {job_config.version} than current 1.1.")
                    console.print("[bold yellow]To get the most functinality, please run `robbie configure` or `robbie run --i` to create the lastest job_config.yaml file.")
                    console.print("[bold yellow]Robbie will attempt run your job with defaults, but some features may not work.")

                    if job_config.python_job.commands:
                        console.print(f"[yellow]job_config.yaml contains the following commands:")
                        for cmd in job_config.python_job.commands:
                            console.print(f"[yellow] {cmd}")
                        console.print(f"[yellow]Defaulting to JobType: BASH_COMMAND_RUNNER")
                        job_config.python_job.job_type = JobRunType.BASH_COMMAND_RUNNER
                        job_config.python_job.mode = GENERIC_MODE
                        if _running_in_conda():
                            console.print("[yellow]Detected you are running in a conda environment...ignoring.")
                        else:
                            console.print("[yellow]Not running in a conda environment...ignoring")
                    else:
                        console.print("[yellow]  - No commands found, defaulting to REMOTE_FUNCTION_CALL")
                        job_config.python_job.job_type = JobRunType.REMOTE_FUNCTION_CALL
                        if _running_in_conda():
                            console.print(f"[yellow]Detected you are running in a conda environment {os.environ['CONDA_PREFIX']}")
                            job_config.python_job.mode = CONDA_MODE
                        else:
                            console.print("[yellow]Not running in a conda environment...ignoring")
                            job_config.python_job.mode = PYTHON_MODE
                    
                    if job_config.python_job.workspace_dir:
                        console.print("[yellow]  - workspace_dir is deprecated. Setting `include_local_dir` = True")
                        job_config.python_job.include_local_dir = True

                elif job_config and job_config.version == 1.1:
                    if job_config.python_job.workspace_dir:
                        console.print("[yellow]  - workspace_dir is deprecated. Please use include_local_dir instead.")
                        job_config.include_local_dir = True

                if job_config.python_job.name:
                    job_config.python_job.name_selection = f"from {config_path}"
                if job_config.python_job.funding_group_id:
                    job_config.python_job.funding_selection = f"from {config_path}"
                if job_config.python_job.environment_id:
                    job_config.python_job.environment_selection = f"from {config_path}"
                if job_config.python_job.image:
                    job_config.python_job.image_selection = f"from {config_path}"
                if job_config.python_job.dependencies:
                    job_config.python_job.dep_selection = f"from {config_path}"
                if job_config.python_job.rpv:
                    job_config.python_job.rpv_selection = f"from {config_path}"
                if job_config.python_job.include_local_dir:
                    job_config.python_job.include_local_dir_selection = f"from {config_path}"
                if job_config.python_job.mode:
                    job_config.python_job.mode_selection = f"from {config_path}"

                return job_config.python_job
            else:
                return None

    except Exception as e:
        raise Exception(e)



def merge_from_yaml_and_args(
    input_job_config: Union[PositronJob, None],
    args_job_config: Union[PositronJob, None]
) -> PositronJob:
    """
    Merge the job_config (from the yaml or empty object) file with the command line arguments for funding, environment, and image.
    Ensure that environment is in the funding group.

    Behavior:
    - Command line arguments take precedence over the job_config.yaml file
    - Command line arguments are not memorized in the job_config.yaml file 
    - Defaults are applied where selections are missing

    """
    # if arges_job_config is None, then we are not using the command line arguments
    name_arg = args_job_config.name if args_job_config else None
    funding_arg = args_job_config.funding_group_id if args_job_config else None
    environment_arg = args_job_config.environment_id if args_job_config else None
    image_arg = args_job_config.image if args_job_config else None
    include_local_dir_arg = args_job_config.include_local_dir if args_job_config else None
    dependencies_arg = args_job_config.dependencies if args_job_config else None
    mode_arg = args_job_config.mode if args_job_config else None
    rpv_arg = args_job_config.rpv if args_job_config else None
    
    # handle case when input is None (no job_config.yaml file)
    if not input_job_config:
        logger.debug("No input_job_config, creating a new PositronJob()")
        return_config = PositronJob()
    else:
        return_config = copy.deepcopy(input_job_config)
    
    logger.debug(f"return_config: {id(return_config)} created from input_job_config: {id(input_job_config)}")

     # 
     # Name
     #
    if return_config.name:
        if name_arg:
            logger.debug(f"Overriding return_config.name: {return_config.name} <-- name_arg: {name_arg}")
            return_config.name = name_arg
            return_config.name_selection = "overridden by argument"
    else:
        if name_arg:
            logger.debug(f"Setting return_config.name: <-- name_arg: {name_arg}")
            return_config.name = name_arg
            return_config.name_selection = args_job_config.name_selection
    #
    # Remote Python Version
    #
    if return_config.rpv:
        # set in the .yaml?
        if rpv_arg:
            logger.debug(f"Overriding return_config.rpv: {return_config.rpv} <-- rpv_arg: {rpv_arg}")
            return_config.rpv = rpv_arg
            return_config.rpv_selection = "overridden by argument"
    else:
        if rpv_arg:
            logger.debug(f"Setting return_config.rpv: <-- rpv_arg: {rpv_arg}")
            return_config.rpv = rpv_arg
            return_config.rpv_selection = "set by argument"
        else:
            return_config.rpv = "local"
    #
    # Include Local Dir
    #
    if return_config.include_local_dir:
        if include_local_dir_arg:
            logger.debug(f"Overriding return_config.include_local_dir: {return_config.include_local_dir} <-- include_local_dir_arg: {include_local_dir_arg}")
            return_config.include_local_dir = include_local_dir_arg
            return_config.include_local_dir_selection = "overridden by argument"
    else:
        if include_local_dir_arg:
            logger.debug(f"Setting return_config.include_local_dir: <-- include_local_dir_arg: {include_local_dir_arg}")
            return_config.include_local_dir = include_local_dir_arg
            return_config.include_local_dir_selection = args_job_config.include_local_dir_selection
    
    #
    # Mode
    #
    if return_config.mode:
        if mode_arg:
            logger.debug(f"overriding return_config.mode: {return_config.mode} <-- mode_arg: {mode_arg}")
            return_config.mode = mode_arg

    else:
        if mode_arg:
            logger.debug(f"setting return_config.mode_arg: <-- mode_arg: {mode_arg}")
            return_config.mode = mode_arg

    #
    # Dependencies
    #
    if return_config.dependencies:
        if dependencies_arg:
            logger.debug(f"overriding return_config.dependencies: {return_config.dependencies} <-- dependencies_arg: {dependencies_arg}")
            return_config.dependencies = dependencies_arg
            return_config.dep_selection = "overridden by argument"
    else:
        if dependencies_arg:
            logger.debug(f"setting return_config.dependencies: <-- dependencies_arg: {dependencies_arg}")
            return_config.dependencies = dependencies_arg
            return_config.dep_selection = "set by argument"

    # 
    # Funding Group
    #
    if return_config.funding_group_id:
        if funding_arg:
            logger.debug(f"Setting or overriding return_config.funding_group_id: {return_config.funding_group_id} <-- funding_arg: {funding_arg}")
            return_config.funding_group_id = funding_arg
            return_config.funding_selection = "overridden by argument"
        else:
            logger.debug(f"return_config.funding_group_id: already set: {return_config.funding_group_id}")
            # ok the correct funding group is already in return_config.funding_group_id
            pass
    else:
        if funding_arg:
            logger.debug(f"Setting return_config.funding_group_id: {return_config.funding_group_id} <-- funding_arg: {funding_arg}")
            return_config.funding_group_id = funding_arg
            return_config.funding_selection = "setting by argument"
        else:
            # no funding group id in job_config.yaml or argument
            logger.debug(f"No funding group id in job_config.yaml or argument")
        
    # pre-fetch the funding sources info and def env
    fs = list_funding_sources()
    if len(fs) == 0:
        logger.debug("No funding sources found.")
        return None

    def_env_id = None
    # Have we identified a funding group yet?
    if return_config.funding_group_id:
        logger.debug(f"Yes, we have a funding group: {return_config.funding_group_id}")
        if not return_config.environment_id:
            for _, val in fs.items():
                if (val[FS_ID] == return_config.funding_group_id):
                    def_env_id = val.get(FS_DEF_ENV_ID)
            if not def_env_id:
                console.print(f"[bold red]Can't get the default environment for the funding group: {return_config.funding_group_id}")
                return None   
            if not return_config.environment_id:
                logger.debug(f"setting return_config.environment_id: {return_config.environment_id} <-- def_env_id: {def_env_id}")
                return_config.environment_id = def_env_id
                return_config.environment_selection = "default"
        else:
            if not environment_arg and (not _env_in_funding_group(return_config.environment_id, return_config.funding_group_id)):
                console.print(f"[bold red] Sorry, the environment in your job_config.yaml: {return_config.environment_id} is not in the funding group: {return_config.funding_group_id}")
                return None
    else: 
        # No funding group id, let's get the user's personal and defaut environment
        logger.debug("Still no funding group id, let's get the user's personal one.")
        for _, val in fs.items():
            if (val[FS_TYPE] == FS_PERSONAL_TYPE):
                return_config.funding_group_id = val.get(FS_ID)
                def_env_id = val.get(FS_DEF_ENV_ID)
                logger.debug(f"Setting return_config.funding_group_id to PERSONAL: {return_config.funding_group_id}, fetched def_env_id: {def_env_id}")
        if return_config.funding_group_id:
            return_config.funding_selection = "default"
        else:
            console.print("[bold red]Can't get the default funding source (personal).")
            return None
        if not def_env_id:
            console.print("[bold red]Can't get the default environment for the personal funding source.")
            return None
        # the user specified an environment in the job_config.yaml file
        if return_config.environment_id:
            # just for fun, lets check if its in the funding group
            if not environment_arg and (not _env_in_funding_group(return_config.environment_id, return_config.funding_group_id)):
                console.print(f"[bold red] Sorry, the environment in your job_config.yaml: {return_config.environment_id} is not in the funding group: {return_config.funding_group_id}")
                return None
        else:
            logger.debug(f"setting return_config.environment_id: {return_config.environment_id} <-- def_env_id: {def_env_id}")
            return_config.environment_id = def_env_id
            return_config.environment_selection = "default from Funding Source"
        
    # At this point we should have a funding group id and a default environment id
    if environment_arg:
        # check to make certain the environment argument is in the funding group
        if not _env_in_funding_group(environment_arg, return_config.funding_group_id):
            console.print(f"[bold red] Sorry, the environment you passed as an argument: {environment_arg} is not in the funding group: {return_config.funding_group_id}")
            return None
        logger.debug(f"setting return_config.environment_id: {return_config.environment_id} <-- environment_arg: {environment_arg}")
        return_config.environment_id = environment_arg
        return_config.environment_selection = "overridden by argument"

    # Use configured image or auto-select
    if return_config.image and not image_arg:
        logger.debug(f'Using the image: {return_config.image}. To override, please use the --image option.')
        return_config.image_selection = f"from {return_config.filename}"
    elif return_config.image and image_arg:
        logger.debug(f'overriding image: {return_config.image}, setting image to: {image_arg}')
        return_config.image = image_arg
        return_config.image_selection = "overridden by argument"
    elif not return_config.image and image_arg:
        logger.debug(f'setting image: {return_config.image}, setting image to: {image_arg}')
        return_config.image = image_arg
        return_config.image_selection = "set by argument"
    elif not return_config.image:
        logger.debug(f'No image found, setting to auto-select')
        return_config.image = "auto-select"
        
    logger.debug(return_config.to_string("Exiting _merge_from_yaml_and_args()"))

    return return_config

def _env_in_funding_group(env_id, funding_group_id):
    """ sanity check a environment id is in the funding group """
    
    if env_id == "auto-select":
        return True
    try :
        envs = list_environments(funding_group_id)
        for _, val in envs.items():
            if (val[FS_ID] == env_id):
                return True
        return False
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}")
        return False

# if main then load and validate
''''
if __name__ == "__main__":
    job_config = load_job_config()
    if job_config:
        job_config.validate_values()
        print(job_config)
'''
