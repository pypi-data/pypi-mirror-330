import os
from common.console import console, ROBBIE_BLUE, ROBBIE_DEFAULT
from rich.prompt import Confirm
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import Validator
from prompt_toolkit.completion import WordCompleter
from common.config import PositronJob, PositronJobConfig
from common.enums import JobRunType
from common.utils import _current_python_version, _valid_python_versions
from common.image_name import get_auto_image_name_and_cluster
from positron_job_runner.runtime_environment_manager import (
     RuntimeEnvironmentManager,
    _running_in_conda,
    _get_python_version_from_conda_yaml,
    CONDA_MODE,
    PYTHON_MODE,
    GENERIC_MODE
)
from cli.helpers import (
    FundingSources,
    Environments,
    Images
)

def prompt_and_build_positron_job_config(
    job_config_yaml: PositronJob = None,
    cmd_runner_dash_i: bool = False
) -> PositronJobConfig:
    """
    Prompts the user, in the command line, for parameters to run a job and returns a PositronJobConfig object.
    This function is invoked in two ways:
    - from `run.py` - for command line or notebook runner jobs - `cmd_runner_dash_i` is True
    - from `configure.py` - to build job_config.yaml for all job types (Runner and Remote Function) - `cmd_runner_dash_i` is False
    """
 
    while True:
        try:

            pj = PositronJob()

            style = Style.from_dict({
                'completion-menu.completion': 'bg:#008888 #ffffff',
                'completion-menu.completion.current': 'bg:#00aaaa #000000',
            })

            if not cmd_runner_dash_i:
                # User selects the job type
                job_type_list = [
                    "Command Runner",
                    "Remote Function"
                ]
                def is_job_type_valid(text):
                    return text == "" or text in job_type_list

                job_type_validator = Validator.from_callable(
                    is_job_type_valid, 
                    error_message="Please choose a valid job type."
                )
                job_type_selection = prompt(
                    message=_blue_msg("Choose a job type", f"{job_type_list[0]}"),
                    completer=WordCompleter(job_type_list), 
                    style=style, 
                    validator=job_type_validator
                )
                if job_type_selection == "":
                    pj.job_type = JobRunType.BASH_COMMAND_RUNNER
                elif job_type_selection == job_type_list[0]:
                    pj.job_type = JobRunType.BASH_COMMAND_RUNNER
                elif job_type_selection == job_type_list[1]:
                    pj.job_type = JobRunType.REMOTE_FUNCTION_CALL
                else:
                    console.print("[yellow]Invalid job type, aborting and starting over.[/yellow]")
                    continue
            else:
                # we are in command line mode, so we know the job type
                pj.job_type = JobRunType.BASH_COMMAND_RUNNER


            # now ask for the mode depdending on the job type
            if pj.job_type == JobRunType.BASH_COMMAND_RUNNER:
                mode_list = [
                    "Generic",
                    "Conda (Python and Non-Python)", 
                    "Python (Non-Conda)", 
                ]
 
                def is_mode_valid(text):
                    return text == "" or text in mode_list

                mode_validator = Validator.from_callable(
                    is_mode_valid, 
                    error_message="Please choose a valid mode."
                )
                mode_selection = prompt(
                    message=_blue_msg(
                        "Choose an environment for the remote machine:", 
                        f"{mode_list[0]}"
                    ),
                    completer=WordCompleter(mode_list), 
                    style=style, 
                    validator=mode_validator
                )
                if mode_selection == "":
                    pj.mode = GENERIC_MODE
                elif mode_selection == mode_list[0]:
                    pj.mode = GENERIC_MODE
                elif mode_selection == mode_list[1]:
                    pj.mode = CONDA_MODE
                elif mode_selection == mode_list[2]:
                    pj.mode = PYTHON_MODE
                else:
                    console.print("[red]Invalid mode, aborting and starting over.[/red]")
                    continue

            elif pj.job_type == JobRunType.REMOTE_FUNCTION_CALL:
                # remote function
                mode_list = [
                    "Conda (Python and Non-Python)",
                    "Python (Non-Conda)", 
                ]
                def is_mode_valid(text):
                    return text == "" or text in mode_list

                mode_validator = Validator.from_callable(
                    is_mode_valid, 
                    error_message="Please choose a valid mode."
                )
                mode_selection = prompt(
                    message=_blue_msg(
                        "Choose an environment for the remote machine:", 
                        f"{mode_list[0]}"
                    ),
                    completer=WordCompleter(mode_list), 
                    style=style, 
                    validator=mode_validator
                )
                if mode_selection == "":
                    pj.mode = CONDA_MODE
                elif mode_selection == mode_list[0]:
                    pj.mode = CONDA_MODE
                elif mode_selection == mode_list[1]:
                    pj.mode = PYTHON_MODE
                else:
                    console.print("[red]Invalid mode, aborting and starting over.[/red]")
                    continue
            else:
                console.print("[red]Invalid job type, aborting and starting over.[/red]")
                continue

            #
            # Conda
            #
            if pj.mode == CONDA_MODE:
                # Let the user select the conda environment, either the current environment or from a yaml file

                # if _running_in_conda():
                #    console.print(f"Conda environment detected: {os.getenv('CONDA_DEFAULT_ENV')}") 

                conda_env_list = _get_files_with_extensions(".", [".yml", ".yaml"])
                if _running_in_conda():
                    conda_env_list.extend([f"auto-capture"])
        
                def is_conda_env_valid(text):
                    return text == "" or text in conda_env_list

                conda_env_validator = Validator.from_callable(
                    is_conda_env_valid, 
                    error_message='Please choose a valid conda environment or file.'
                )

                conda_env = prompt(
                    message=_blue_msg("Choose a conda environment [.yml/.yaml] file", f"auto-capture"),
                    completer=WordCompleter(conda_env_list), 
                    style=style, 
                    validator=conda_env_validator
                )
 
                # Only indicate we have deps if the user selects something
                if len(conda_env):
                    pj.dependencies = conda_env
                    pj.dep_selection = "user selected"
                elif conda_env == "":
                    pj.dependencies = "auto-capture"
                    pj.dep_selection = "default"
                else:
                    console.print(f"[red]Error: You must select a valid conda environment or file.")
                    continue

            elif pj.mode == PYTHON_MODE:

                if pj.job_type == JobRunType.BASH_COMMAND_RUNNER:
                # Only allow Python version changes in the command runner mode        
                    def is_python_version_valid(text):
                        return text == "" or text == "local" or text in _valid_python_versions()

                    python_version_validator = Validator.from_callable(
                        is_python_version_valid, 
                        error_message="Please choose a valid Python version or none."
                    )
                    wclist = _valid_python_versions()
                    wclist.append("local")

                    python_version_selection = prompt(
                        message=_blue_msg("Choose Python version", 
                                          "local"
                        ),
                        completer=WordCompleter(wclist), 
                        style=style, 
                        validator=python_version_validator
                    )
                    # If the user explicitly selects a different version, set it in the job config
                    if (python_version_selection == "" or 
                        python_version_selection == "local"
                    ):
                        pj.rpv = "local"
                    else:
                        pj.rpv = python_version_selection
                        pj.rpv_selection = "user selected"
                elif pj.job_type == JobRunType.REMOTE_FUNCTION_CALL:
                    pj.rpv = "local"
                else:
                    console.print("[red]Invalid job type, aborting and starting over.")
                    continue
                # 
                # Dependencies
                # 
                # python deps - requirements.txt or auto-capture
                py_deps_list = _get_files_with_extensions(".", [".txt"])
                if (pj.rpv == _current_python_version() or 
                    pj.rpv == "local"):
                    py_deps_list.extend(["auto-capture","none"])
                else:
                    py_deps_list.extend(["none"])
        
                def is_dependency_valid(text):
                    return text == "" or text in py_deps_list

                dependency_validator = Validator.from_callable(
                    is_dependency_valid, 
                    error_message='Please choose a valid selection.'
                )

                deps = prompt(
                    message=_blue_msg(
                        "Choose Python dependencies: ", 
                        "requirements.txt"
                    ),
                    completer=WordCompleter(py_deps_list), 
                    style=style, 
                    validator=dependency_validator
                )
                # only indicate we have deps if the user selects something
                if len(deps):
                    pj.dependencies = deps
                    pj.dep_selection = "user selected"
                elif deps == "":
                    pj.dependencies = "requirements.txt"
                    pj.dep_selection = "default"
                else:
                    console.print(f"[red]Error: You must select a valid Python dependency file.")
                    continue
            elif pj.mode == GENERIC_MODE:
                # default out for image selection
                pj.rpv = "local"
            else:
                console.print("[yellow]Invalid mode, aborting and starting over.[/yellow]")
                continue

            # Get the user's funding sources
            try:
                fs = FundingSources.load()
                if fs == None:
                    console.print(f"[bold red]User has no funding sources, please contact: support@robbie.run")
                    return None
            except Exception as e:
                console.print(f"[bold red]Unable to fetch funding sources: {e}") 
                return None

            # validate the user input
            def is_fs_valid(text):
                return text == "" or text in fs.menu_items()
            
            fs_validator = Validator.from_callable(
                is_fs_valid, 
                error_message='Please select a valid funding source.'
            )

            fs_choice = prompt(
                message=_blue_msg("Select how to bill your job", "Personal tokens"),
                completer=WordCompleter(fs.menu_items()), 
                style=style, 
                validator=fs_validator
            )

            if len(fs_choice):
                fs_id = fs.id_from_menu_item(fs_choice)
                pj.funding_selection = "user selected"
            else:
                fs_id = fs.default_funding_source_id()
                pj.funding_selection = "default"

            pj.funding_group_id = fs_id

            #
            # Environments
            #

            # are there any environments in this funding source?
            try:
                envs = Environments.load(pj.funding_group_id)
                if envs == None:
                     # no environments for the user oh well
                    console.print(f"[red]Error your environments: {fs_choice} has no approved hardware, please contact 'support@robbie.run'")
                    return None
            except Exception as e:
                console.print(f"[bold red]Unable to fetch environments: {e}") 
                return None

            # validate the user input
            def is_env_valid(text):
                return text == "" or text in envs.menu_items() or text == "Automatically select using AI (experimental)"
            env_validator = Validator.from_callable(
                is_env_valid, 
                error_message='Please enter a valid environment.'
            )

            env_menu_items = envs.menu_items()
            env_menu_items.append("Automatically select using AI (experimental)")

            env_choice = prompt(
                message=_blue_msg("Select your preferred hardware", 
                                    ("None" 
                                    if not fs.default_env_name_from_fs_id(fs_id) 
                                    else fs.default_env_name_from_fs_id(fs_id))
                ), 
                completer=WordCompleter(env_menu_items), 
                style=style, 
                validator=env_validator)

            if len(env_choice):
                if env_choice == "Automatically select using AI (experimental)":
                    pj.environment_id = "auto-selected"
                    pj.environment_selection = "auto-selected (experimental)"
                else:
                    pj.environment_id = envs.id_from_menu_item(env_choice)
                    pj.environment_selection = "user selected"
            else:
                # choose the default, if available
                if fs.default_env_id_from_fs_id(fs_id) == None:
                    console.print(f"[red] Error funding source: {fs_choice} has no default hardware and you didn't specify any.")
                    return None
                else:
                    pj.environment_id = fs.default_env_id_from_fs_id(fs_id)
                    pj.environment_selection = "default"

            # 
            # Include Local directory 
            #
            pj.include_local_dir = False
            text = prompt(
                message=_blue_msg(f"Copy local CWD to be copied to the remote machine?", "[y]/n"),
                style=style)
            if len(text):
                if text.lower() == "y":
                    pj.include_local_dir = True
            else:
                pj.include_local_dir = True
        
            # advanced options include: image selecdtion, max tokens, max duration, and environment variables
            if Confirm.ask("Configure advanced options?", default=False):
                if pj.include_local_dir:
                    #
                    # Custom file filters
                    #
                    first_pass = True
                    while True:
                        ignore_patten = prompt('Enter file patterns to ignore (Enter a <blank> line to go to the next step):',
                                          style=Style.from_dict({'prompt': ROBBIE_BLUE})
                        )
                        if ignore_patten == "":
                            break
                        if first_pass:
                            pj.custom_file_filter = []
                            first_pass = False
                        pj.custom_file_filter.append(ignore_patten)

                #
                # Images
                #
                images = Images.load(pj.funding_group_id, pj.environment_id)
                def is_image_valid(text):
                    return (text == "" 
                            or text == "auto-select" 
                            or text in images.menu_items()
                    )

                image_validator = Validator.from_callable(
                    is_image_valid, 
                    error_message='Please choose a valid image.'
                )

                if images:
                    image_list = images.menu_items()
                    image_list.append("auto-select")
                    image_choice = prompt(message=_blue_msg("Select your preferred image", "auto-select"),
                                          completer=WordCompleter(image_list), 
                                          style=style, 
                                          validator=image_validator
                    )

                    if image_choice == "" or image_choice == "auto-select":
                        # the actual image selection occurs in `run.py`
                        pj.image = "auto-select"
                        pj.image_selection = "default"
                    elif len(image_choice) and image_choice != "auto-select":
                        # the user hit tab and selected an image
                        pj.image = images.name_from_menu_item(image_choice)
                        # we just get the cluster type from the environment
                        pj.cluster = envs.cluster_type_from_env_id(pj.environment_id)
                        pj.image_selection = "user selected"
                else:
                    # no environments for the user oh well
                    console.print(f"[red]Failed to get images, please contact 'support@robbie.run'")
                    return None
            
                # 
                # Max tokens
                #
                def is_max_token_valid(text):
                    return text == "" or (text.isdigit() and int(text) >=1 and int(text) < 10000)

                max_token_validator = Validator.from_callable(is_max_token_valid, 
                                                              error_message='Please enter a number between 1 and 10000.'
                )

                text = prompt(
                    message=_blue_msg("Maximum tokens to consume", "none"),
                    style=style, 
                    validator=max_token_validator
                )
                if len(text):
                    pj.max_tokens = int(text)

                # 
                # Max duration
                #
                def is_max_duration_valid(text):
                    return text == "" or (text.isdigit() and int(text) >=1 and int(text) < 1000)
                duration_validator = Validator.from_callable(is_max_duration_valid, error_message='Please enter a valid duration between 1 and 1000.')

                text = prompt(
                    message=_blue_msg("Max duration in minutes", "none"),
                    style=style, 
                    validator=duration_validator)

                if len(text):
                    pj.max_time = int(text)

                # 
                # Environment variables
                #
                preserve = False
                if job_config_yaml and job_config_yaml.env:
                    console.print(f"[yellow]{job_config_yaml.filename} contains the following environment variables:")
                    for env in job_config_yaml.env:
                        console.print(f"[yellow]     {env}")
                    response = prompt('Reuse for this run? [[y]/n]:', style=Style.from_dict({'prompt': 'yellow'}))
                    if response in ["y", "yes", "Yes", "Y", ""]:
                        preserve = True  
                        pj.env = job_config_yaml.env 

                if not preserve:
                    first_pass = True
                    while True:
                        var_name = prompt('Environment variable name (Enter a <blank> line to go to the next step):',
                                          style=Style.from_dict({'prompt': ROBBIE_BLUE})
                        )
                        if not var_name:
                            break
                        var_value = prompt(f'Value for {var_name} (hint= Enter a <blank> line to use local machine value):', style=style)
                        if first_pass:
                            pj.env = {}
                            first_pass = False
                        pj.env[var_name] = var_value
            else:
                pj.image = "auto-select"
                pj.image_selection = 'Automatically Selected'

            # 
            # Commands - loop through and capture the commands
            #
            if pj.job_type == JobRunType.BASH_COMMAND_RUNNER:
                msg = "Enter the commands to run on the remote machine (Enter a <blank> line when you are done entering commands):"
                preserve = False
                if job_config_yaml and job_config_yaml.commands:
                    console.print(f"[yellow]{job_config_yaml.filename} contains the following commands:")
                    for cmd in job_config_yaml.commands:
                        console.print(f"[yellow]     {cmd}")
                    response = prompt('Reuse for this run? [[y]/n]:', style=Style.from_dict({'prompt': 'yellow'}))
                    if response in ["y", "yes", "Yes", "Y", ""]:
                        preserve = True
                        pj.commands = job_config_yaml.commands        

                if not preserve:
                    first_pass = True
                    while True:
                        cmd = prompt(msg, style=Style.from_dict({'prompt': ROBBIE_BLUE}))
                        if not cmd:
                            break
                        if first_pass:
                            pj.commands = []
                            first_pass = False
                        pj.commands.append(cmd)

            # user can enter a name
            name_choice = prompt(
                _blue_msg("Please enter a custom run name", "Robbie Generated"),
                style=style)
            if len(name_choice):
                pj.name = name_choice

            # print(f"End of Interactive Job Config: {pj.to_string()}")

            return PositronJobConfig(version="1.1", python_job=pj)

        except (KeyboardInterrupt, EOFError) as e:
            console.print("[yellow]Aborting job configuration.")
            return None


def _blue_msg(message, default):
    """
    Helper function to build a prompt with the ROBBIE blue color
    """
    msg = [ 
        (ROBBIE_BLUE, f"{message} ["),
        (ROBBIE_DEFAULT, default),
        (ROBBIE_BLUE, "]: " )
        ]
    return msg


def _get_files_with_extensions(directory, extensions_to_include):
    """Gets a list of files in the directory, include  specified extensions."""
    all_files = os.listdir(directory)
    # use list comprehension to filter out files with the wrong extensions
    filtered_files = [
        file
        for file in all_files
        if os.path.splitext(file)[1].lower() in extensions_to_include
    ]
    return filtered_files


def get_job_config_yaml_name():

    style = Style.from_dict({
        'completion-menu.completion': 'bg:#008888 #ffffff',
        'completion-menu.completion.current': 'bg:#00aaaa #000000',
    })

    def is_job_config_valid(text):
        return text == "" or text == "e" or text.endswith(".yaml") or text.endswith(".yml")
    
    jc_validator = Validator.from_callable(
        is_job_config_valid, 
        error_message='Please enter a valid file name!'
    )

    while True:
        jc_name = prompt(
            message=_blue_msg("Specify a file name to save your job configuration or (e) to exit without saving: ", "job_config.yaml"), 
            style=style, 
            validator=jc_validator
        )
        if jc_name == "e":
            return None
        if jc_name == "":
            jc_name = "job_config.yaml"
    
        if os.path.isfile(jc_name):
            if Confirm.ask(f"File {jc_name} already exists. Overwrite?", default=False):
                return jc_name
            else:
                console.print("[yellow]Try again.")
        else:
            return jc_name




    

