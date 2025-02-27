import os
import typer
import pyfiglet
import re
import pprint
import platform
import tempfile
import shutil
from git import Repo
from rich.prompt import Confirm
from rich.spinner import Spinner
from rich.live import Live
from rich.text import Text
from typing_extensions import Annotated
from common.console import console
from common.constants import JOB_CONF_YAML_PATH
from common.observability.main import track_command_usage
from cli.interactive import (
    prompt_and_build_positron_job_config,
    get_job_config_yaml_name
)
from common.console import console, ROBBIE_BLUE, ROBBIE_DEFAULT
from common.api.get_env_rec import get_env_rec
from common.api.funding_envs_images import *
from cli.auto_complete import (
    funding_group_auto_complete,
    job_config_auto_complete,
    cluster_auto_complete,
)
from common.config import (
    load_job_config, 
    PositronJob,
    PositronJobConfig
)
from common.logging_config import logger


SPINNER = "line" if platform.system() == "Windows" else "dots"

@track_command_usage("rec")
def rec(
    python_file: Annotated[str, typer.Argument(help='Python file to analyze')],
    job_config_arg: Annotated[str, 
                            typer.Option("--f", 
                                        help="Specify the job configuration file.",
                                        autocompletion=job_config_auto_complete)] = "./job_config.yaml",
    funding_arg: Annotated[str, typer.Option("--funding_group_id", 
                                help="Specify the team to run the job on.",
                                autocompletion=funding_group_auto_complete)] = None,
    cluster_arg: Annotated[str, 
                        typer.Option("--cluster",
                                        help="Specify the cluster to run the job on.", 
                                        autocompletion=cluster_auto_complete)] = None

) -> None:
    """
    Use GenAI to get an environment recommendation
    """

    ascii_banner = pyfiglet.figlet_format("Robbie")
    console.print(ascii_banner, style='#41a7ff')

    console.print(f"Robbie will use AI to determine the best hardware for you Python program.\n", style=ROBBIE_BLUE)

    global_job_config_yaml = None

    try:
        if funding_arg is None:
        # try to determine FG from job config
            global_job_config_yaml = load_job_config(job_config_arg)
            if global_job_config_yaml:
                logger.debug(f"global_job_config_yaml: {global_job_config_yaml.to_string()}")
                console.print(f"[green]✔[/green] Determining funding_group_id from configuration file: ", end="", style=ROBBIE_BLUE)
                console.print(f"{job_config_arg}", style=ROBBIE_DEFAULT)
                if global_job_config_yaml.funding_group_id:
                    funding_group_id = global_job_config_yaml.funding_group_id
                else:
                    # we need to get the default funding group
                    funding_group_id = _get_personal_fg()
                    if funding_group_id is None:
                        console.print(f"[red]No funding group found. Please specify a funding group.")
                        return
                    console.print(f"[green]✔[/green] Using personal funding group: {funding_group_id}", style=ROBBIE_BLUE)
                    
            else:
                logger.debug(f"{job_config_arg} not found.")
                # we need to get the default funding group
                funding_group_id = _get_personal_fg()
                if funding_group_id is None:
                    console.print(f"[red]No funding group found. Please specify a funding group.")
                    return
                console.print(f"[green]✔[/green] Using personal funding group: {funding_group_id}", style=ROBBIE_BLUE)
                    
        else:
            funding_group_id = funding_arg
            console.print(f"[green]✔[/green] Using funding group argument: {funding_group_id}", style=ROBBIE_BLUE)
                    

        system_prompt, human_prompt = build_prompt_from_envs(funding_group_id, python_file, cluster_arg)
        if human_prompt == "":
            console.print(f"[red]Error - no files to analyze.")
            return

    except Exception as e:
        print(f'Error: {str(e)}')
        return

    with Live(Spinner(SPINNER, text=Text(f"Securely analyzing your code...", style=ROBBIE_BLUE)), refresh_per_second = 20, console=console, transient=True):
        try:
            return_env = get_env_rec(
                system_prompt=system_prompt,
                human_prompt=human_prompt
            )
        except Exception as e:
            console.print(f"Error getting environment recommendation: {str(e)}")
            return

    console.print(f"[green]✔[/green] Analysis Complete!", style=ROBBIE_BLUE)

    console.print(f"[green]✔[/green] Recommanded Environment: ", style=ROBBIE_BLUE)

    console.print(return_env.get("response"))

    uuid = find_uuids(return_env.get("response"))
    if len(uuid)== 1:
        env_id = find_uuids(return_env.get("response"))[0]
    else:
        console.print(f"Error: Could not find a correct number of UUIDs in the response.")
        return

    if Confirm.ask("\nDo you want to save this environment in your job config?", default=False):
        if global_job_config_yaml is None:
            console.print(f"[red]Error: couldn't add environment to existing job configuration file: {job_config_arg}")
            return
        filename = get_job_config_yaml_name()
        if filename:
            global_job_config_yaml.environment_id = env_id
            pjc = PositronJobConfig(version="1.1", python_job=global_job_config_yaml)
            pjc.write_to_file(filename=filename)
            console.print(f"[green]✔[/green] Success!", style=ROBBIE_BLUE)
    return

def extract_gpu_details(gpu_string: str):
    # Enhanced regex to handle more variations in GPU naming
    match = re.search(r'(?P<gpu_type>.+)-(?P<vram>\d+GB)$', gpu_string)
    if match:
        gpu_type = match.group('gpu_type')
        vram = match.group('vram')
        return gpu_type, vram
    else:
        return None, None

# Test with multiple GPU strings
gpu_list = [
    "NVIDIA-A100-SXM4-40GB",
    "NVIDIA-V100-PCIe-16GB",
    "NVIDIA-RTX3090-24GB",
    "NVIDIA-H100-PCIe-80GB",
    "NVIDIA-Tesla-K80-12GB"
]


def get_aws_gpu_details(instance_type: str):
    """
    Returns the GPU type and VRAM size (as a string) for a given AWS instance type.

    Args:
        instance_type (str): The AWS instance type (e.g., 'p4d.24xlarge').

    Returns:
        tuple: (GPU type, VRAM size as a string) or ('Unknown GPU', '0GB') if not found.
    """
    # Mapping of AWS instance families to GPU type and VRAM size (as string)
    aws_gpu_mapping = {
        "p4d": ("NVIDIA A100", "40GB"),
        "p4de": ("NVIDIA A100", "40GB"),
        "p3": ("NVIDIA V100", "16GB"),
        "p3dn": ("NVIDIA V100", "32GB"),
        "p2": ("NVIDIA K80", "12GB"),
        "g4dn": ("NVIDIA T4", "16GB"),
        "g5": ("NVIDIA A10G", "24GB"),
        "g5g": ("NVIDIA T4G", "16GB"),
        "g3": ("NVIDIA M60", "8GB"),
        "g2": ("NVIDIA K520", "4GB"),
        "p5": ("NVIDIA H100", "80GB"),
        "g6": ("NVIDIA L4 Tensor Core", "24GB"),
        "p6": ("NVIDIA H100", "80GB"),
        "g4ad": ("AMD Radeon Pro V520", "8GB"),  # Not NVIDIA, included for completeness
        "dl1": ("Habana Gaudi", "32GB"),        # Not NVIDIA
        "trn1": ("AWS Trainium", "0GB"),        # Not NVIDIA
        "inf1": ("AWS Inferentia", "0GB"),      # Not NVIDIA
    }

    # Extract the portion of the instance name before the dot
    instance_prefix = instance_type.split('.')[0]

    # Retrieve GPU details or return defaults if not found
    return aws_gpu_mapping.get(instance_prefix, ("Unknown GPU", "0GB"))


def _get_personal_fg():
    """
    Get the personal funding group
    """
    fs = list_funding_sources()
    if len(fs) == 0:
        return None
    
    personal_fs_id = None
    for key, val in fs.items():
        if (val[FS_TYPE] == FS_PERSONAL_TYPE):
            personal_fs_id = val.get(FS_ID)
    
    if personal_fs_id is None:
        return None
    else:
        return personal_fs_id


def find_uuids(text):
    """
    Finds all UUIDs in a string.

    Args:
        text: The string to search.

    Returns:
        A list of UUIDs found in the string.
    """
    uuid_pattern = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}"
    return re.findall(uuid_pattern, text, re.IGNORECASE)


def build_prompt_from_envs(funding_group_id: str, python_file: str, cluster_arg: str = None):

    if not is_git_url(python_file):
        if python_file != ".":
            if not os.path.exists(python_file):
                console.print(f"[red]Python file not found: {python_file}")
                raise FileNotFoundError(f"Python file not found: {python_file}")

            if not python_file.endswith(".py") and not python_file.endswith(".ipynb"):
                console.print(f"[red]Python or notebook file must end with .py or .ipynb: {python_file}")
                raise Exception("Python file must end with .py or .ipynb")

    python_code = None

    try:
        if (is_git_url(python_file)):
            python_code = fetch_python_files_from_repo(python_file)
            if python_code == "":
                console.print(f"[red]Error fetching Python files from repo: {python_file}")
                raise Exception(f"Error fetching Python files from repo: {python_file}")
        elif python_file == ".":  # read all python files in the current directory
            python_code = read_python_files()
        elif python_file.endswith(".ipynb") or python_file.endswith(".py"):
            console.print(f"  Files for analysis:", style=ROBBIE_BLUE)
            console.print(f"[yellow] - {python_file}")
            with open(python_file, 'r') as file:
                python_code = file.read()
        else:
            console.print(f"[red]Python file not found: {python_file}")
            raise FileNotFoundError(f"Python file not found: {python_file}")

        # lets build the list of environments to for the prompt
        envs = list_environments(fs_id=funding_group_id)
        if envs is None:
            console.print(f"No environments found for this funding group: {funding_group_id}")
            raise Exception(f"No environments found for this funding group: {funding_group_id}")

        env_entry_list = []
        for key, val in envs.items():
            # print(f"Environment: {val}")
            if cluster_arg is not None and val.get(ENV_CLUSTER_TYPE) != cluster_arg:
                continue
            if not val.get(ENV_DELETED):
                if (val.get(ENV_GPU_NUMBER) == 0 or val.get(ENV_GPU_NUMBER) == None or val.get(ENV_GPU_NUMBER) == ""):
                    gpu_number = "None"
                    gpu_type = "None"
                    gpu_vram = "None"
                else:
                    gpu_number = val.get(ENV_GPU_NUMBER)
                    if val.get(ENV_CLUSTER_TYPE) == "NERC":
                        gpu_type, gpu_vram = extract_gpu_details(val.get(ENV_GPU_TYPE))
                        if gpu_type is None or gpu_vram is None:
                            logger.warning(f"Could not extract GPU details from: {val.get(ENV_GPU_TYPE)}")
                            gpu_type = "None"
                            gpu_vram = "None"
                    elif val.get(ENV_CLUSTER_TYPE) == "EKS":
                        instance_type = val.get(ENV_NODE_TYPE)
                        if instance_type is None or instance_type == "":
                            console.print(f"Instance type not found for environment: {val.get(ENV_ID)}")
                            raise Exception(f"Instance type not found for environment: {val.get(ENV_ID)}")
                        gpu_type, gpu_vram = get_aws_gpu_details(instance_type)
                        if gpu_type is None or gpu_vram is None:
                            logger.warning(f"Could not extract GPU details from: {val.get(ENV_GPU_TYPE)}")
                            gpu_type = "None"
                            gpu_vram = "None"
                    elif val.get(ENV_CLUSTER_TYPE) == "DOCKER":
                        continue
                    else:
                        console.print(f"Unknown cluster type: {val.get(ENV_CLUSTER_TYPE)}")
                        raise Exception(f"Unknown cluster type: {val.get(ENV_CLUSTER_TYPE)}")

                # print(f"id: {val.get(ENV_ID)}, GPU Type: {gpu_type}, VRAM: {gpu_vram}, GPU Number: {gpu_number}\n\n")
                entry = { 
                    "id": val.get(ENV_ID), 
                    "environmentName": val.get(ENV_NAME), 
                    "cpu": val.get(ENV_CPU),
                    "ram": val.get(ENV_RAM),
                    "disk": val.get(ENV_DISK),
                    "gpuNumber": gpu_number,
                    "gpuType": gpu_type,
                    "gpuVRAM": gpu_vram,
                    "tokensPerHour": val.get(ENV_TPH),
                }
                env_entry_list.append(entry)
        if len(env_entry_list) == 0:
            console.print(f"No environments found for this funding group: {funding_arg}")
            raise Exception(f"Instance type not found for environment: {val.get(ENV_ID)}")
    except Exception as e:
        console.print(f'Error loading environments! {str(e)}')
        raise e
        

    # print(pprint.pformat(env_entry_list))

    system_prompt = f"""
You are an automated code analysis tool that looks a Python machine learning source code and makes a recommendation of the hardware to use for training.
Your will choose from a list of available hardware options. 
Each entry in the list will have the following JSON structure.

    "id": a UUID of the hardware, 
    "environmentName": a string representing the name of the hardware,
    "cpu": a string representing the number of virtual CPUs,
    "ram": a string representing the amount of system ram in gigabyes represented as Gi,
    "disk": a string representing the amount of disk space in gigabyes represented as Gi,
    "gpuNumber": a string representing the number of GPUs, "None" if no GPU, 
    "gpuType": a string representing the type of GPU if one exists,
    "gpuVRAM": a string representing the amount of VRAM on the GPU in GB,
    "tokensPerHour": the cost per hour in token to use the hardware

Here is the list: {str(env_entry_list)}
Your goal is to choose the hardware that will train the model the fastest while keeping the cost as low as possible.
I am going to provide Python source code and I want you to return the name, cost, GPU type, GPU VRAM, and UUID of the environment. After a carriage return provide a three sentence explanation of you chose the hardware option.
"""

    human_prompt = f"""{python_code}"""

    return system_prompt, human_prompt


def fetch_python_files_from_repo(repo_url):
    """
    Fetches all python files from a github repo, clones it to a temporary directory,
    reads all of the .py files and returns a string with the files contents.
    
    args:
    repo_url (str): The URL of the GitHub repository.
    
    returns:
    str: A string containing the combined content of all .py files in the repository,
         or an empty string if an error occurs.
    """
    console.print(f"  Files to analyze: {repo_url}", style=ROBBIE_BLUE)
    temp_dir = tempfile.mkdtemp()
    try:
        Repo.clone_from(repo_url, temp_dir)
        python_files_content = ""
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(".py") or file.endswith(".ipynb"):
                    console.print(f"[yellow]  - {file}")
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        python_files_content += f.read() + "\n"
        return python_files_content
    except Exception as e:
         print(f"An error occurred: {e}")
         return ""
    finally:
        shutil.rmtree(temp_dir)


def read_python_files(directory="."):
    """
    Recursively searches for .py files in the given directory and returns their contents as a string.

    Args:
        directory (str, optional): The directory to search in. Defaults to the current directory.

    Returns:
        str: A string containing the contents of all .py files found, separated by newlines.
    """
    console.print(f"  Files to analyze in: {os.getcwd()}", style=ROBBIE_BLUE)
    all_contents = ""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") or file.endswith(".ipynb"):
                console.print(f"[yellow]  - {file}")
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r") as f:
                        contents = f.read()
                        all_contents += contents + "\n"
                except Exception as e:
                    print(f"Error reading file {filepath}: {e}")
    return all_contents


def is_git_url(url: str) -> bool:
    """
    Detects if a string is a valid URL and if it ends with '.git'.

    Args:
        url (str): The URL string to check.

    Returns:
        bool: True if the string is a URL and ends with '.git', False otherwise.
    """
    # Regex pattern to check for valid URL ending with '.git'
    pattern = r'^(https?|git|ssh|ftp)://[^\s]+\.git$'
    return bool(re.match(pattern, url))

