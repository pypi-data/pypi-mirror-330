import os
import re
import typer
import pyfiglet
import platform
from typing_extensions import Annotated
from typing import Optional
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from common.config import (
    PositronJob,
    load_job_config, 
    merge_from_yaml_and_args
)
from common.cli_args import args
from common.console import console, ROBBIE_DEFAULT, ROBBIE_BLUE
from common.constants import JOB_CONF_YAML_PATH
from common.logging_config import logger
from common.enums import JobRunType
from common.image_name import get_auto_image_name_and_cluster
from common.observability.main import track_command_usage
from common.api.funding_envs_images import *
from common.api.get_env_rec import (
    get_env_rec,
)
from cli.cmds.download import filename_is_valid
from cli.cmds.login import login
from cli.deploy import command_runner_deploy
from cli.cmds.rec import (
    build_prompt_from_envs,
    find_uuids
)
from cli.interactive import (
    prompt_and_build_positron_job_config,
    get_job_config_yaml_name
)
from common.env_defaults import current
from cli.auto_complete import (
    funding_group_auto_complete, 
    environment_auto_complete, 
    images_auto_complete,
    deps_auto_complete,
    job_config_auto_complete,
    cluster_auto_complete,
)
from positron_job_runner.runtime_environment_manager import (
    RuntimeEnvironmentManager, 
    _build_job_args, 
    _running_in_conda,
    _get_python_version_from_conda_yaml,
    CONDA_MODE,
    PYTHON_MODE,
    GENERIC_MODE
)

#
# Naming convention for the arguments:
#
# `jctr` is the PositronJob object that will be passed to deploy to run the job
# `rpv` is the Python version to run the job on the remote machine
# `deps` is the file containing the dependencies or auto-capture
#

@track_command_usage("run")
def run(
  # the following options control the job configuration
  job_config_arg: Annotated[str, 
                            typer.Option("--f", 
                                        help="Specify the job configuration file.",
                                        autocompletion=job_config_auto_complete)] = "./job_config.yaml",
  name_arg: Annotated[str, typer.Option("--name", help="Name of the run")] = None,
  funding_arg: Annotated[str, 
                         typer.Option("--funding_group_id", 
                                help="Specify the team to run the job on.",
                                autocompletion=funding_group_auto_complete)] = None,
  environment_arg: Annotated[str, 
                             typer.Option("--environment_id", 
                                    help="Specify the hardware to run the job on.",
                                    autocompletion=environment_auto_complete)] = None,
  image_arg: Annotated[str, 
                       typer.Option("--image", 
                            help="Specify the image to run the job on or 'auto-select'.",
                            autocompletion=images_auto_complete)] = None,
  commands: Annotated[Optional[str], typer.Argument(help='Shell command(s)')] = None,
  depfile_arg: Annotated[str, 
                         typer.Option("--deps", 
                                      help='Specify the file containing the deps or auto-capture.',
                                      autocompletion=deps_auto_complete)] = None,
  conda_arg: Annotated[bool, typer.Option("--conda", help='Run on remote machine in a conda environment')] = None,
  python_arg: Annotated[bool, typer.Option("--python", help='Run on remote machine in a Python environment', is_flag=False)] = None,
  python_ver_arg: Annotated[str, typer.Option("--version", help='Specify the Python version to run the job on.')] = None,    
  include_local_dir_arg: Annotated[bool, typer.Option("--include-local-dir", help='Include the working directory in the job.')] = False,

  cluster_arg: Annotated[str, typer.Option("--cluster",
                                        help="Specify the cluster to run the job on.", 
                                        autocompletion=cluster_auto_complete)] = None,

    
  # the following options control how the job is run
  tail: Annotated[bool, typer.Option("--tail", help='Tail the run\'s stdout back to your CLI.')] = False,
  skip_prompts: Annotated[bool, typer.Option("--y", help='Bypass the prompts and execute the run immediately.')] = False,
  interactive: Annotated[bool, typer.Option("--i", help="Interactively choose your run configuration.")] = False,
  download: Annotated[str, typer.Option("--download", help="Download a results <file> to your local machine. Specify 'all' for the complete list.")] = None,
  path: Annotated[str, typer.Option("--path", help="Local directory where the downloaded files will be stored.")] = None,
  create_only: Annotated[bool, typer.Option("--create-only", help="Only create the run, do not execute it. [Robbie internal use only]")] = False,
  local_container: Annotated[str, typer.Option("--local", help="Run the job in a local container <path of source>. [Robbie internal use only]")] = False,
  verbose: Annotated[bool, typer.Option("--v", help="Show advanced details.")] = False,
) -> None:
    """
    Run shell commands as a batch job in Robbie

    There are three possible scenarios:
    1. User types: robbie run - commands are run from the job_config.yaml file
    2. User types: robbie run "command" - commands override the job_config.yaml file
    3. User types: robbie run --i - interactive mode, user is prompted for all the options and a job_config.yaml file is created/overwritten

    In scenerio 1 and 2, user's can pass in funding groups and enviroments as arguments to override the job_config.yaml file.

    """
    ascii_banner = pyfiglet.figlet_format("Robbie")
    console.print(ascii_banner, style='#41a7ff')

    console.print(f"[blue]Platform: [white]{platform.system()}[blue] Stage: [white]{current.name}")
    if platform.system() == "Windows" and os.getenv('CONDA_DEFAULT_ENV'):
        console.print(f"[yellow] Windows conda support is currently experimental.")

    logger.debug(f"""========== run() arguments ==========
    - name_arg: {name_arg}
    - funding_arg: {funding_arg}
    - environment_arg: {environment_arg}
    - image_arg: {image_arg}
    - commands: {commands}
    - depfile_arg: {depfile_arg}
    - conda_arg: {conda_arg}
    - python_arg: {python_arg}
    - include_local_dir_arg: {include_local_dir_arg}
    - verbose: {verbose}
    - tail: {tail}
    - skip_prompts: {skip_prompts}
    - interactive: {interactive}
    - download: {download}
    - path: {path}
    - create_only: {create_only}
    - local_container: {local_container}""")

    # check if the user is logged in
    login()

    console.print("[green]✔[/green] Current working directory: ", os.getcwd(), style=ROBBIE_BLUE)
    # was there a job_config.yaml file in the CWD?

    try:
        global_job_config_yaml = load_job_config(job_config_arg)
        if global_job_config_yaml:
            logger.debug(f"global_job_config_yaml: {global_job_config_yaml.to_string()}")
            console.print(f"[green]✔[/green] Loaded run configuration file: ", end="", style=ROBBIE_BLUE)
            console.print(f"{job_config_arg}", style=ROBBIE_DEFAULT)
            if global_job_config_yaml.job_type != JobRunType.BASH_COMMAND_RUNNER:
                console.print(f"[red]Error, {job_config_arg} file is not configured for bash command runner.")
                return
        else:
            console.print(f"[yellow]{job_config_arg} not found.")
            logger.debug(f"{job_config_arg} not found.")
    except Exception as e:
        print(f'Error loading job configuration! {str(e)}')
        return

    if _running_in_conda():
        console.print(f"[green]✔[/green] Running in conda environment: {os.getenv('CONDA_DEFAULT_ENV')}", style=ROBBIE_BLUE)
    else:
        console.print(f"[green]✔[/green] Running in non-conda environment", style=ROBBIE_BLUE)

    
    if (download and not tail):    
        console.print('[red]Error: The --download option can only be used with the --tail')
        return
    
    if download and not filename_is_valid(download):
        console.print('[red]Error: Please specify a valid file name or "all" to download all files.')
        return
    
    if path and not download:
        console.print('[red]Error: The --path option can only be used with the --download option.')
        return
    
    if path and not os.path.exists(path):
        console.print('[red]Error: The path you specified is not valid.')
        return

    # initialize the argument singleton
    args.init(
        name=name_arg,
        stream_stdout=tail,
        skip_prompts=skip_prompts,
        commands_to_run=commands,
        interactive=interactive,
        create_only=create_only,
        local_container=local_container,
        download=download,
        local_path=path,
    )

    # first-level sanity checks
    if commands and interactive:
        console.print("[red]Sorry: Please specify command line or use the interactive mode.")
        return
    
    if interactive and (funding_arg or environment_arg or image_arg):
        console.print("[red]Sorry: You can't specify funding, environments, or images in interactive mode.")
        return
    
    if conda_arg and interactive:
        console.print("[red]Sorry: You can't specify remote conda mode in interactive mode.")
        return
    
    if python_arg and interactive:
        console.print("[red]Sorry: You can't specify remote Python modde in interactive mode.")
        return
    
    if depfile_arg and interactive:
        console.print("[red]Sorry: You can't specify deps in interactive mode.")
        return
    
    if conda_arg and python_arg:
        console.print("[red]Sorry: You can't specify conda and python modes at the same time.")
        return
    
    if conda_arg and python_ver_arg:
        console.print("[red]Sorry: You can't specify a Python version with conda mode.")
        return
    
    # capture arguments job configuration
    job_config_args = PositronJob()
    if name_arg:
        job_config_args.name = name_arg
    if funding_arg:
        job_config_args.funding_group_id = funding_arg
        job_config_args.funding_selection = "Passed as argument to the run command"
    if environment_arg:
        job_config_args.environment_id = environment_arg
        job_config_args.environment_selection = "Passed as argument to the run command"
    if image_arg:
        job_config_args.image = image_arg
        job_config_args.image_selection = "Passed as argument to the run command"
    if depfile_arg:
        job_config_args.dependencies = depfile_arg
        job_config_args.dep_selection = "Passed as argument to the run command"
    if conda_arg:
        job_config_args.mode = CONDA_MODE
    if python_arg:
        job_config_args.mode = PYTHON_MODE
    if python_ver_arg:
        job_config_args.rpv = python_ver_arg
    if include_local_dir_arg:
        job_config_args.include_local_dir = include_local_dir_arg

    # print(f"job_config_args: {job_config_args.to_string()}")

    """
    There are three possible scenarios:
    1. User types: robbie run - commands are run from the job_config.yaml file
    2. User types: robbie run "command" - commands override the job_config.yaml file
    3. User types: robbie run --i - interactive mode, user is prompted for all the options and a job_config.yaml file is created

    There are three important variables in the code:
    - global_job_config_yaml - this is the PositronJob object created from the job_config.yaml file
    - jctr - this is the PositronJob object that will be passed to deploy to run the job
    - scenerio_1_and_2 - this is a flag that is set for scenerio 1 and 2 to merge the passed arguments into to the jctr object
    """
    scenerio_1_and_2 = False

    # Scenerio 1: User types: "robbie run" - commands are run from the job_config.yaml file
    #
    if not commands and not interactive:
        logger.debug("@@@@@@@@@@@   Scenerio 1: User types: robbie run")
        if not global_job_config_yaml:
            console.print('[red]Error: No job_config.yaml file found or it is invalid. Cannot find commands to run.')
            return
        if not global_job_config_yaml.commands:
            console.print('[red]Error: No commands found in job_config.yaml file.')
            return
        jctr = global_job_config_yaml.deepcopy()
        scenerio_1_and_2 = True

    # Scenerio 2. User types: robbie run "command" - commands override the job_config.yaml file if it exists
    #
    if commands:
        logger.debug("@@@@@@@@@@ Scenerio 2: User types: robbie run 'command'")

        # Is there a job_config.yaml file?
        if global_job_config_yaml:
            if global_job_config_yaml.commands:
                console.print('[yellow] Overriding commands in existing job_config.yaml file.')
            jctr = global_job_config_yaml.deepcopy()
        else:
            jctr = PositronJob()
        
        # Add the commands to the job_config
        jctr.commands = []
        jctr.commands.append(commands)

        scenerio_1_and_2 = True
        
    # now lets deal with the arguments for the first two scenarios
    if scenerio_1_and_2:

        logger.debug(f"scenerio_1_and_2 - jctr: {jctr.to_string()}")
        # Determine the version of Python to use for the job on the remote machine
        # Normally, the user doesnt' touch this and the Python version is picked up from the local environment by default

        # other arguments are merged into the jctr object
        logger.debug("Adding arguments to job_config")
        jctr = merge_from_yaml_and_args(jctr, job_config_args)
        if not jctr:
            logger.debug('[red]Error: Unable to merge yaml and arguments.')
            return
     
    # Scenerio 3. User types: robbie run --i - interactive mode, user is prompted for all the options and a job_config.yaml file is created or modified
    if interactive:
        logger.debug("@@@@@@@@@ Scenerio 3: User types: robbie run --i")

        # lets prompt the user 
        console.print(f"\nPlease follow the prompts to configure your run ([{ROBBIE_DEFAULT}][] = default[/{ROBBIE_DEFAULT}], <tab> for menu, contol-c to exit):", style=ROBBIE_BLUE)
        captured_job_config = prompt_and_build_positron_job_config(
            cmd_runner_dash_i = True,
            job_config_yaml=global_job_config_yaml, 
        )
        if captured_job_config == None:
            console.print(f"[red]Sorry, failed to create a file {JOB_CONF_YAML_PATH}")
            return
        
        logger.debug(f"Interactive cfg: {captured_job_config.python_job.to_string()}")
        # print(f"Interactive cfg: {captured_job_config.python_job.to_string()}")

        if captured_job_config.python_job.commands == None:
            console.print("[red]Error: You did not specify any commands to run.")
            return
        
        filename = get_job_config_yaml_name()
        if filename:
            captured_job_config.write_to_file(filename=filename)
            jctr = captured_job_config.python_job.deepcopy()

     # verbose logs
    if verbose:
        jctr.verbose = True

    # 
    #  Sort out the mode based on deps and Python environment.
    #
    # - CONDA_MODE - Remote runs as a mirror to the local conda environment (Python version and deps)
    # - PYTHON_MODE - Remote runs as a mirror to the local Python environment (Python version and deps)
    # - GENERIC_MODE - Remote runs whatever we specify (Python version and deps)
    #
    # Deal with no mode specified in the job_config.yaml file or the arguments
    # print(f"jctr.mode: {jctr.mode}")
    
    # Note used - if mode wasn't set, his code attempts to infer the mode based on the deps
    
    # Was a mode ever set in job_config.yaml or args, if not default to GENERIC
    if not jctr.mode:
        jctr.mode = GENERIC_MODE

    console.print("Robbie is analyzing run information...", style=ROBBIE_BLUE) 

    if jctr.mode == CONDA_MODE:
        # you want to run in a conda environment
        logger.debug(f"Conda mode: jctr.dependencies: {jctr.dependencies}")
        if not (jctr.dependencies and 
          (jctr.dependencies == "auto-capture" or
            jctr.dependencies.endswith(".yml") or 
            jctr.dependencies.endswith(".yaml"))):
            console.print("[red]Error: You specified 'conda' mode but did not provide a valid conda environment file or specify auto-capture.")
            return
        
        # Set python version based on the environment .yaml
        if (jctr.dependencies and 
            (jctr.dependencies.endswith('.yaml') or 
             jctr.dependencies.endswith(".yml"))
        ):
            yaml_py_vers = _get_python_version_from_conda_yaml(jctr.dependencies)
            if yaml_py_vers:
                # deal with possible 3-digit versions (e.g. 3.10.15)
                yaml_py_vers = convert_to_two_digit_version(yaml_py_vers)
                # console.print(f"Python version: {yaml_py_vers} detected in conda yaml file: {jctr.dependencies}")
                jctr.rpv = yaml_py_vers
                jctr.rpv_selection = f"detected in conda environment file: {jctr.dependencies}"
            else:
                # No python in the .yaml, default to 3.10 for image selection
                jctr.rpv = "3.10"
                jctr.rpv_selection = "default for image selection"

        elif jctr.dependencies == "auto-capture":
            # if we are auto-capturing get the python version from the conda env
            if _running_in_conda():
                 # console.print("Auto-capturing Python version from conda environment....")
                conda_py_vers = RuntimeEnvironmentManager()._python_version_in_conda_env(os.getenv('CONDA_DEFAULT_ENV'))
                 # console.print(f"Python version: {conda_py_vers} detected in environment: {os.getenv('CONDA_DEFAULT_ENV')}")
                if conda_py_vers:
                    jctr.rpv = conda_py_vers
                    jctr.rpv_selection = f"detected in conda environment: {os.getenv('CONDA_DEFAULT_ENV')}"
                    console.print(f"[green]✔[/green] Determined Python version: {jctr.rpv} from conda environment: {os.getenv('CONDA_DEFAULT_ENV')}", style=ROBBIE_BLUE)
                else:
                    jctr.rpv = "3.10"
                    jctr.rpv_selection = "default for image selection"
            else:
                console.print(f"[red]Error: You are not running in a conda environment, please start over and select a .yaml file.")
                return
        else:
            console.print(f"[red]Error: You must select a valid conda environment or file.")
            return
        
    elif jctr.mode == PYTHON_MODE:
        # you want to run non-conda python
        logger.debug(f"Python mode: jctr.dependencies: {jctr.dependencies}, jctr.dep_selection: {jctr.dep_selection}")
        # python version not set
        if not jctr.rpv:
            console.print("[red]Error: PYTHON_MODE, rpv should be set.")
            return
        elif jctr.rpv == "local":
            jctr.rpv = RuntimeEnvironmentManager()._current_python_version()
            jctr.rpv_selection = "local environment"
            console.print(f"[green]✔[/green] Determined local Python version: {jctr.rpv}", style=ROBBIE_BLUE)
        if jctr.dependencies:
            if jctr.dependencies == "auto-capture":
                if _running_in_conda():
                    console.print("[red]Error: You specified 'python' mode auto-capture in a conda environment.")
                    return
                if jctr.rpv != "local" and jctr.rpv != RuntimeEnvironmentManager()._current_python_version():
                    console.print("[red]Error: You can't auto-capture deps and specify a Python version other than the local one.")
                    return
            if not (jctr.dependencies in ["auto-capture", "requirements.txt", "none"]):
                console.print("[red]Error: You specified 'python' mode but did not specify a valid requirements.txt file or auto-capture.")
                return
        # else:
        #    console.print("[red]Error: You specified 'python' mode but did not provide a valid requirements.txt file or specify auto-capture.")
        #    return
    elif jctr.mode == GENERIC_MODE:
        # setting this purely to help with image selection, nothing else
        if not jctr.rpv:
            console.print("[red]Error: GENERIC_MODE, rpv should be set.")
            return
        elif jctr.rpv == "local":
            jctr.rpv = RuntimeEnvironmentManager()._current_python_version()
            jctr.rpv_selection = "local environment"
    else:
        console.print("[red]Error: Invalid mode. Please specify 'conda', 'python', or 'generic'.")
        return

    # 
    # Dependencies - Handle auto capturing deps 
    # 
    if jctr.dependencies == "auto-capture":
        jctr.dep_selection = "auto-captured"
    
    if jctr.dependencies == "none":
        jctr.dep_selection = "Not specified"
        jctr.dependencies = None

    # snapshot() does a couple of things: 1) verifies that a passed file exists; 2) auto-captures deps if needed
    try:
        jctr.dependencies = RuntimeEnvironmentManager().snapshot(jctr.dependencies)
    except Exception as e:
        console.print(f"[red]Error: {e}")
        return
    console.print("[green]✔[/green] Dependencies and environment captured.", style=ROBBIE_BLUE)

    #
    # Auto-detect the environment
    #
    if jctr.funding_group_id:
        if jctr.environment_id == "auto-select":
            # if there a python file we can analyze
            python_file = None
            for cmd in jctr.commands:
                python_file = find_python_file_name(cmd)
                if python_file:
                    break
            if not python_file:
                console.print(f"[red]Error: You selected `auto-select` but we cannot find a Python file in the commands.")
                return

            retun_env = None
            try:
                console.print(f"Using AI to securely determine the best hardware for your workload...", style=ROBBIE_BLUE)
                system_prompt, human_prompt = build_prompt_from_envs(jctr.funding_group_id, python_file, cluster_arg)
                if human_prompt == "":
                    console.print(f"[red]Error - no files to analyze.")
                    return
                return_env = get_env_rec(
                    system_prompt=system_prompt,
                    human_prompt=human_prompt
                )
            except Exception as e:
                console.print(f"Error getting environment recommendation: {str(e)}")
                return

            console.print(f"Analysis Complete!", style=ROBBIE_BLUE)

            uuid = find_uuids(return_env.get("response"))
            if len(uuid)== 1:
                env_id = find_uuids(return_env.get("response"))[0]
            else:
                console.print(f"Error: Could not find a correct number of UUIDs in the response.")
                return
            console.print(f"[green]✔[/green] Recommanded Environment: {env_id}", style=ROBBIE_BLUE)
            jctr.environment_id = env_id
            jctr.environment_selection = "auto-selected using AI (experimental)"

    #
    # Image selection
    #
    if jctr.image == "auto-select":
        jctr.image, jctr.cluster = get_auto_image_name_and_cluster(
            jctr.funding_group_id, 
            jctr.environment_id,
            jctr.rpv
        )
        jctr.image_selection = "auto-selected"
        # console.print('Auto-selecting image:', style=ROBBIE_BLUE, end="")
        # console.print(f'{jctr.image} on {jctr.cluster} cluster', style=ROBBIE_DEFAULT)
        console.print("[green]✔[/green] Automatically selected image", style=ROBBIE_BLUE)

    # this will be psssed to the job runner
    args.job_args = _build_job_args(
        mode = jctr.mode,
        rpv = jctr.rpv,
        dependencies = jctr.dependencies,
    )
    logger.debug(f"job_args: {args.job_args}")

    jctr.job_type = JobRunType.BASH_COMMAND_RUNNER

    logger.debug("Calling command_runner_deploy")
    command_runner_deploy(jctr)

def _remove_package_from_requirements(package_name, file_path='./requirements.txt'):
    """ this is hack when the robbie package gets auto-added to the requirements.txt file in the auto-capture deps mode """
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Write back all lines except the one with the package name
    with open(file_path, 'w') as file:
        for line in lines:
            if not line.strip().startswith(package_name):
                file.write(line)

def convert_to_two_digit_version(version: str) -> str:
    """
    Converts a three-digit version number (e.g., 1.2.3) to a two-digit version (e.g., 1.2).
    """
    parts = version.split(".")
    # just return the version if it's already two digits
    if len(parts) == 2:
        return version
    elif len(parts) == 3:
        return f"{parts[0]}.{parts[1]}"
    else:
        raise ValueError(f"Invalid version format: {version}")


def find_python_file_name(text):
    """
    Checks if a string contains a Python file name and returns the file name if found.

    Args:
        text: The string to search within.

    Returns:
        The Python file name (including the .py extension) if found, otherwise None.
    """
    match = re.search(r"(\w+)\.py\b", text)
    if match:
        return match.group(0)
    return None
