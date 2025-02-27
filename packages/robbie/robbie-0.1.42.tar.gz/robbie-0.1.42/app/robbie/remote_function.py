import os
import argparse
import pyfiglet
import platform
from functools import wraps
from common.cli_args import args as cli_args
from common.config import (
    PositronJob, 
    merge_from_yaml_and_args,
    load_job_config
)
from remote_function.deploy import Deploy
from remote_function.stored_function import StoredFunction
from common.observability.main import track_command_usage
from common.image_name import get_auto_image_name_and_cluster
from common.user_config import user_config
from common.console import console, ROBBIE_BLUE
from common.logging_config import logger, set_log_level
from common.enums import JobRunType
from common.utils import _exit_by_mode, _nb
from common.env_defaults import current
from robbie.notebook_cell_ui import notebook_cell_ui
from cli.cmds.login import login
from positron_job_runner.runtime_environment_manager import (
    RuntimeEnvironmentManager, 
    _build_job_args, 
    _running_in_conda,
    CONDA_MODE,
    PYTHON_MODE,
    GENERIC_MODE
)

def remote(**parameters):
    """
    Decorator to deploy a function in Robbie. 
    This works in both a Jupyter notebook and a Python script.

    You can pass argumments to the decorator to customize the deployment in two ways:
    - Command Line Arguments when running from the commmand line - e.g. python my_script.py --tail
        Supported arguments:
            --tail: bool
            --loglevel: str [CRITICAL,FATAL,ERROR, WARNING, INFO, DEBUG, NOTSET]
            --create-only: bool
            - local_container: str (path to your distribution)
            --results-from-job-id: str (job_id )
    - Decorator Aguments in a Python script or Jupyter Notebook when decorating a function - e.g. @remote(tail=True)
        Supported arguments:
            - funding_group_id: str
            - environment_id: str
            - image: str
            - tail: bool    
            - loglevel: str
            - create_only: bool
            - chooser_ui: bool (Enable user to choose job config via a small GUI in the cell - Used in Jupyter Notebook only)

    """
    if not os.getenv('POSITRON_CLOUD_ENVIRONMENT'):
        # Parse command line arguments
        parser = argparse.ArgumentParser(description = "A decorator to handle deploying running your function in the cloud")
        parser.add_argument('--f', type=str, help='Path to job_config.yaml file', dest='job_config_arg', default='./job_config.yaml')
        parser.add_argument('--tail', action='store_true', help='Stream the stdout from Robbie back to your cli', dest='stream_stdout', default=False)
        parser.add_argument('--loglevel', help='Set the logging level [CRITICAL,FATAL,ERROR, WARNING, INFO, DEBUG, NOTSET]')
        parser.add_argument('--create-only', action='store_true', help='Create the job but do not run it.', dest='create_only')
        parser.add_argument('--local', type=str, help='Run job on local container <path to distribution>', dest='local_container')
        parser.add_argument('--results-from-job-id', help='Fetch results and return from decorated function.')
        parser.add_argument('--v', action='store_true', help='Verbose logging.', dest='verbose')
        positron_args, _ = parser.parse_known_args()

        verbose_arg = False

        if positron_args.loglevel:
            set_log_level(positron_args.loglevel)
        if positron_args.verbose:
            verbose_arg = True

        ascii_banner = pyfiglet.figlet_format("Robbie")
        console.print(ascii_banner, style='#41a7ff')

        console.print(f"[blue]Platform: [white]{platform.system()}[blue] Stage: [white]{current.name}")
        if platform.system() == "Windows" and os.getenv('CONDA_DEFAULT_ENV'):
            console.print(f"[yellow] Windows conda support is currently experimental.")

        logger.debug("========positron_args========")
        # print("positron_args=", positron_args)
        logger.debug(positron_args) 

        # Jupyter Support - Default out the cli_args to run remote always with no prompting
        if not cli_args.is_init:
            cli_args.init(
                local=False,
                deploy=True,
                stream_stdout=positron_args.stream_stdout,
                create_only=positron_args.create_only,
                local_container=positron_args.local_container,
                results_from_job_id=positron_args.results_from_job_id,
                skip_prompts=True,
            )

        chooser_ui_flag = False
        # enable  and tail function parameters but remove them before passing to PositronJob config
        if "loglevel" in parameters:
            set_log_level(parameters["loglevel"])
            del parameters["loglevel"]
        if "tail" in parameters:
            cli_args.stream_stdout = parameters["tail"]
            del parameters["tail"]
        if "create_only" in parameters:
            cli_args.create_only = parameters["create_only"]
            del parameters["create_only"]
        if "results_from_job_id" in parameters:
            cli_args.results_from_job_id = parameters["results_from_job_id"]
            del parameters["results_from_job_id"]
        if "chooser_ui" in parameters:
            chooser_ui_flag = True
            del parameters["chooser_ui"]
        if "verbose" in parameters:
            verbose_arg = True
            del parameters["verbose"]

        console.print("[green]✔[/green] Current working directory: ", os.getcwd(), style=ROBBIE_BLUE)
        
        # was there a job_config.yaml file in the CWD?
        try: 
            global_job_config_yaml = load_job_config(positron_args.job_config_arg)
            if global_job_config_yaml:
                logger.debug(f"global_job_config_yaml: {global_job_config_yaml.to_string()}")
                console.print(f"[green]✔[/green] Loaded run configuration file: ", end="", style=ROBBIE_BLUE)
                console.print(f"{positron_args.job_config_arg}")
                if global_job_config_yaml.job_type != JobRunType.REMOTE_FUNCTION_CALL:
                    console.print(f"[red]Error, job_config.yaml file is not configured for a remote function.")
                    return
            else:
                console.print("[yellow] No job_config.yaml file found.")
                logger.debug("No job_config.yaml file found.")
        except Exception as e:
            print(f'Error loading job configuration! {str(e)}')
            return

        # print(f"global_job_config_yaml: {global_job_config_yaml.to_string()}")

        if _running_in_conda():
            console.print(f"[green]✔[/green] Running in conda environment: {os.getenv('CONDA_DEFAULT_ENV')}", style=ROBBIE_BLUE)
        else:
            console.print(f"[green]✔[/green] Running in non-conda environment", style=ROBBIE_BLUE)


    def decorator(func):
        @track_command_usage("remote")
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug("Running decorator")

            if os.getenv('POSITRON_CLOUD_ENVIRONMENT'):
                logger.debug("Running function locally")
                return func(*args, **kwargs)

            # This check eliminates a extra step if the user happens to run robbie run and the API key is not valid
            login()

            if cli_args.results_from_job_id:
                stored_function = StoredFunction(func, args, kwargs)
                stored_function.set_job_id(cli_args.results_from_job_id)
                secret_key = user_config.user_auth_token if user_config.user_auth_token else ""
                stored_function.load_and_validate_results(hmac_key=secret_key)
                return stored_function.result

            # get decorator arguments
            job_config = None
            job_config_ui_or_arguments = None
            nonlocal chooser_ui_flag
            
            if chooser_ui_flag:
                if _nb: # we are in a notebook
                    job_config_ui_or_arguments = notebook_cell_ui()
                    if job_config_ui_or_arguments == None:
                        console.print("[red] User interrupted.")
                        return
                else:
                    console.print("[yellow]Warning: The 'chooser_ui' is only supported in Jupyter Notebooks. Please remove this argument.[/yellow]")
                    logger.warning("Warning: The 'chooser_ui' is only supported in Jupyter Notebooks. Please remove this argument.")
                    _exit_by_mode(1)
                logger.debug(job_config_ui_or_arguments.to_string("job_config_ui_or_arguments (arguments passed into remote function)"))
            else:
                job_config_ui_or_arguments = PositronJob(**parameters)
                if job_config_ui_or_arguments == None:
                    console.print("[red]Failed to create PositronJob from @remote parameters.")
                    return
                
                # print(f"job_config_ui_or_arguments: {job_config_ui_or_arguments.to_string()}")
                
                if job_config_ui_or_arguments.rpv:
                    console.print("[red]Error: The 'python_version' argument is not supported with remote functions.\nPlease remove it.[/red]")
                    _exit_by_mode(1)

                # track where the parameters come from so we can display to the user later
                if job_config_ui_or_arguments.name:
                    # console.print(f"name: {job_config_ui_or_arguments.name} - argument to @remote decorator.")
                    job_config_ui_or_arguments.name_selection = "argument to @remote decorator"
                if job_config_ui_or_arguments.funding_group_id:
                    # console.print(f"funding_group_id: {job_config_ui_or_arguments.funding_group_id} - argument to @remote decorator.")
                    job_config_ui_or_arguments.funding_selection = "argument to @remote decorator"
                if job_config_ui_or_arguments.environment_id:
                    # console.print(f"environment_id: {job_config_ui_or_arguments.environment_id} - argument to @remote decorator.")
                    job_config_ui_or_arguments.environment_selection = "argument to @remote decorator"
                if job_config_ui_or_arguments.image:
                    # console.print(f"image: {job_config_ui_or_arguments.image} - argument to @remote decorator.")
                    job_config_ui_or_arguments.image_selection = "argument to @remote decorator"
                if job_config_ui_or_arguments.dependencies:
                    # console.print(f"deps: {job_config_ui_or_arguments.dependencies} - argument to @remote decorator.")
                    job_config_ui_or_arguments.dep_selection = "argument to @remote decorator"
                if job_config_ui_or_arguments.include_local_dir:
                    # console.print(f"include_local_dir: {job_config_ui_or_arguments.include_local_dir} - argument to @remote decorator.")
                    job_config_ui_or_arguments.include_local_dir_selection = "argument to @remote decorator"


                logger.debug(job_config_ui_or_arguments.to_string("job_config_ui_or_arguments (arguments passed into remote function)"))


            if global_job_config_yaml and global_job_config_yaml.rpv:
                console.print("[red]Error: You cannot set 'rpv' in job_config.yaml. Please remove it.[/red]")

            job_config = merge_from_yaml_and_args(global_job_config_yaml, job_config_ui_or_arguments)

            if not job_config:
                console.print('[red]Error: Unable to merge yaml and arguments/ui selection.')
                return

            if job_config.commands:
                console.print("[red]Error: The 'commands' configuration in job_config.yaml is not supported in the remote decorator.\nPlease remove it or run with 'robbie run' to use 'commands'.[/red]")
                logger.error("The 'commands' configuration in job_config.yaml is not supported in the remote decorator.")
                _exit_by_mode(1)

            if job_config.rpv and job_config.rpv != "local":
                console.print("[yellow]Warning: You cannot set the remote python in the job_config.yaml or argument when running a remote function...ignoring.\n")
                logger.error("The 'python_version' configuration in job_config.yaml is not supported in the remote decorator.")
                _exit_by_mode(1)
        
            job_config.job_type = JobRunType.REMOTE_FUNCTION_CALL
            job_config.rpv = RuntimeEnvironmentManager()._current_python_version()
            job_config.rpv_selection = "Auto-detected from local machine"
            logger.debug(job_config.to_string("job_config being passed to function"))

            # run with no job_config.yaml or agument
            if not job_config.mode:
                if _running_in_conda():
                    job_config.mode = CONDA_MODE
                    job_config.mode_selection = "not set, auto-detected"
                else:
                    job_config.mode = PYTHON_MODE
                    job_config.mode_selection = "not set, auto-detected"
                
            # if deps are not set, auto-capture
            if not job_config.dependencies:
                console.print(f"No deps set, auto-capturing deps", style=ROBBIE_BLUE)
                job_config.dependencies = "auto-capture"

            if job_config.dependencies == "auto-capture":
                job_config.dep_selection = "auto-captured"

            # sanity checking
            if _running_in_conda() and job_config.mode == PYTHON_MODE:
                console.print("[red]Error: You can't run a non-conda Python job in a conda environment.[/red]")
                _exit_by_mode(1)

            # sanity checking
            if not _running_in_conda() and job_config.mode == CONDA_MODE:
                # we have a problem if we are in a non-conda environment
                console.print("[red]Error: You can't specify conda deps in non-conda environment. Please use requirement.txt[/red]")
                _exit_by_mode(1)

            console.print("Robbie is analyzing run information...", style=ROBBIE_BLUE)

            # snapshot_freeze() does all of the dependency capturing
            job_config.dependencies = RuntimeEnvironmentManager().snapshot(job_config.dependencies)

            if _running_in_conda() and job_config.dependencies.endswith(".txt"):
                console.print("[red]Error: You can't use a requirements.txt file in a conda environment. Please use a .yaml file instead.[/red]")
                _exit_by_mode(1)
            
            if not _running_in_conda() and (job_config.dependencies.endswith(".yml") or job_config.dependencies.endswith(".yaml")):
                console.print("[red]Error: You can't specify conda deps in non-conda environment. Please use requirement.txt[/red]")
                _exit_by_mode(1)
            console.print("[green]✔[/green] Determined environment", style=ROBBIE_BLUE)

            #
            # Image selection
            #
            if job_config.image == "auto-select":
                job_config.image, job_config.cluster = get_auto_image_name_and_cluster(
                    job_config.funding_group_id, 
                    job_config.environment_id,
                    job_config.rpv
                )
                job_config.image_selection = "auto-selected"
                # console.print('Auto-selecting image:', style=ROBBIE_BLUE, end="")
                # console.print(f'{jctr.image} on {jctr.cluster} cluster', style=ROBBIE_DEFAULT)
                console.print("[green]✔[/green] Automatically selected image", style=ROBBIE_BLUE)


            # note: we have changed the behavior or job_args
            cli_args.job_args = _build_job_args(
                mode = job_config.mode,
                rpv = job_config.rpv, 
                dependencies = job_config.dependencies
            )
            logger.debug(f"job_args: {cli_args.job_args}")

            # verbose printouts
            if verbose_arg:
                job_config.verbose = True

            console.print(f"Robbie is running your function remotely!", style="bold")
            return Deploy.remote_function_deploy(func, args, kwargs, job_config)

        return wrapper
    return decorator