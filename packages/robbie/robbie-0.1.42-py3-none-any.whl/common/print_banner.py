import time
import os
from rich import box
from rich.text import Text
from rich.panel import Panel
from rich.console import Group
from rich.tree import Tree
from common.config import PositronJob
from common.console import console, ROBBIE_ORANGE, ROBBIE_BLUE
from common.exceptions import RemoteCallException
from common.logging_config import logger
from common.enums import JobRunType
from positron_job_runner.runtime_environment_manager import (
    _running_in_conda, 
    CONDA_MODE,
    PYTHON_MODE,
    GENERIC_MODE
)
from common.utils import _current_python_version

workspace_file_tree = Tree("Files to be copied to remote machine:", style=ROBBIE_BLUE)

def print_robbie_configuration_banner(job: dict, job_config: PositronJob):

    # print(f"print_robbie_configuration_banner cfg: {job_config.to_string()}")

    text = Text(end="")

    if job_config.name:
        text.append("Run Name: ", style=ROBBIE_BLUE)
        text.append(f"{job_config.name}\n")

    text.append("Run Type: ", style=ROBBIE_BLUE)
    if job_config.job_type == JobRunType.BASH_COMMAND_RUNNER:
        text.append("/bin/bash command runner\n")
        text.append("Remote Mode: ", style=ROBBIE_BLUE)
        if job_config.mode == CONDA_MODE:
            if job_config.mode_selection:
                text.append(f"Conda - {job_config.mode_selection}\n")
            else:
                text.append(f"Conda\n")
            text.append("Remote Python Version: ", style=ROBBIE_BLUE)
            text.append(f"{job_config.rpv} - {job_config.rpv_selection}\n")  
            text.append("Environment file: ", style=ROBBIE_BLUE)
            if not job_config.dependencies:
                text.append("None specified\n")
            else:
                text.append(f"{job_config.dependencies} - {job_config.dep_selection}\n")
        elif job_config.mode == PYTHON_MODE:
            if job_config.mode_selection:
                text.append(f"Python - {job_config.mode_selection}\n")
            else:
                text.append(f"Python\n")
            text.append("Remote Python Version: ", style=ROBBIE_BLUE)
            text.append(f"{job_config.rpv} - {job_config.rpv_selection}\n")  
            text.append("Dependency file: ", style=ROBBIE_BLUE)
            if not job_config.dependencies:
                text.append("None specified\n")
            else:
                text.append(f"{job_config.dependencies} - {job_config.dep_selection}\n")
        elif job_config.mode == GENERIC_MODE:
            text.append(f"Generic\n")
        else:
            console.print(f"[bold red]Unknown command runner mode: {job_config.mode}")
            return
    elif job_config.job_type == JobRunType.REMOTE_FUNCTION_CALL:
        text.append("Remote Function\n")
        text.append("Remote Mode: ", style=ROBBIE_BLUE)
        if job_config.mode == CONDA_MODE:
            if job_config.mode_selection:
                text.append(f"Conda - {job_config.mode_selection}\n")
            else:
                text.append(f"Conda\n")
            text.append("Remote Python Version: ", style=ROBBIE_BLUE)
            text.append(f"{job_config.rpv} - {job_config.rpv_selection}\n")  
            text.append("Environment file: ", style=ROBBIE_BLUE)
            if not job_config.dependencies:
                text.append("None specified\n")
            else:
                text.append(f"{job_config.dependencies} - {job_config.dep_selection}\n")
        elif job_config.mode == PYTHON_MODE:
            if job_config.mode_selection:
                text.append(f"Python - {job_config.mode_selection}\n")
            else:
                text.append(f"Python\n")
            text.append("Remote Python Version: ", style=ROBBIE_BLUE)
            text.append(f"{job_config.rpv} - {job_config.rpv_selection}\n")  
            text.append("Dependency file: ", style=ROBBIE_BLUE)
            if not job_config.dependencies:
                text.append("None specified\n")
            else:
                text.append(f"{job_config.dependencies} - {job_config.dep_selection}\n")
    else:
        console.print(f"[bold red]Unknown job type: {job_config.job_type}")
        return

    text.append("Robbie Python SDK Version: ", style=ROBBIE_BLUE)
    text.append(f"{job_config.robbie_sdk_version}\n")
    
    text.append("Funding Source: ", style=ROBBIE_BLUE)
    if not job_config.funding_selection:
        job_config.funding_selection = "Default"
    if job_config.verbose:
        text.append(f"{job['fundingGroupName']} ({job['fundingGroupId']}) - {job_config.funding_selection}\n")
    else:
        text.append(f"{job['fundingGroupName']} - {job_config.funding_selection}\n")
        
    text.append("Hardware: ", style=ROBBIE_BLUE)
    if not job_config.environment_selection:
        job_config.environment_selection = "Default"
    if job_config.verbose:
        text.append(f"{job['environmentName']} ({job['environmentId']}) - {job_config.environment_selection}\n")
    else:
        text.append(f"{job['environmentName']} - {job_config.environment_selection}\n")

    if job_config.cluster:
        text.append("Cluster: ", style=ROBBIE_BLUE)
        text.append(f"{job_config.cluster}\n")
        
    text.append("Image: ", style=ROBBIE_BLUE)
    if not job_config.image_selection:
        job_config.image_selection = "Default" 
    text.append(f"{job['imageName']} - {job_config.image_selection}\n")

    # max token limit
    if job["maxUsableTokens"]:
        text.append("Max Token Consumption: ", style=ROBBIE_BLUE)
        text.append(f"{job['maxUsableTokens']}\n")
    elif job_config.verbose:
        text.append("Max Token Consumption: ", style=ROBBIE_BLUE)
        text.append("Not specified\n")

    # max time limit
    if job["maxExecutionMinutes"]:
        text.append("Max Execution Time (minutes): ", style=ROBBIE_BLUE)
        text.append(f"{job['maxExecutionMinutes']}\n")
    elif job_config.verbose:
        text.append("Max Execution Time (minutes): ", style=ROBBIE_BLUE)
        text.append("Not specified\n")

    # environment variables
    if job_config.env:
        text.append("Environment Variables: ", style=ROBBIE_BLUE)
        text.append(f"{job_config.env}\n")
    elif job_config.verbose:
        text.append("Environment Variables: ", style=ROBBIE_BLUE)
        text.append(" Not specified\n")

    # shell commands
    if job_config.job_type == JobRunType.REMOTE_FUNCTION_CALL:
        if job_config.commands:
            text.append("Pre-exection shell commands:  \n", style=ROBBIE_BLUE)
            for cmd in job_config.commands:
                text.append(f' - {cmd}\n')
        elif job_config.verbose:
            text.append("No pre-exec shell commands specified\n")
    elif job_config.job_type == JobRunType.BASH_COMMAND_RUNNER:
        if job_config.commands:
            text.append("Shell commands:  \n", style=ROBBIE_BLUE)
            for cmd in job_config.commands:
                text.append(f' - {cmd}\n')
        elif job_config.verbose:
            text.append("No shell commands specified\n")
    else:
        console.print(f"[bold red]Unknown job type: {job_config.job_type}")
        return
    
    # workspace directory
    text.append(f"Copy local CWD to remote machine: ", style=ROBBIE_BLUE)
    text.append(f"{job_config.include_local_dir}\n") 

    if job_config.include_local_dir:
        # custom file filter
        if job_config.custom_file_filter:
            text.append("Custom file filters (exclude):\n", style=ROBBIE_BLUE)
            for f in job_config.custom_file_filter:
                text.append(f" - {f}\n")

        group = Group(text, workspace_file_tree, fit=False)
    else:
        group = Group(text, fit=False)

    console.print(Panel(
        group,
        box=box.ROUNDED,
        # padding=(1, 2),
        title = Text(f"Robbie Run Configuration ({job['tokenRatePerHour']} tokens/hour)", style=ROBBIE_ORANGE),
        border_style=ROBBIE_ORANGE,
    ))
    logger.debug(f"========== Robbie Run Configuration ({job['tokenRatePerHour']} tokens/hour) ========== \n{text}")

def print_job_details_banner(job: dict):
    ## print job details
    text = Text()
    text.append("Run Name: ", style=ROBBIE_BLUE)
    text.append(f"{job['name']}\n")
            
    text.append("Run ID: ", style=ROBBIE_BLUE)
    text.append(f"{job['id']}\n")
        
    text.append("Start Time: ", style=ROBBIE_BLUE)
    text.append(f"{time.asctime()}")

    console.print(Panel(
        text,
        box=box.ROUNDED,
        title=Text("Run Details", style=ROBBIE_ORANGE),
        border_style=ROBBIE_ORANGE,
    ))
    logger.debug(f"\n========== Run Details ========== \n{text}")
    
# prints a rich job completion banner
def print_job_complete_banner(job: dict, start):
    ## print job details
    text = Text()
    text.append("Job Name: ", style=ROBBIE_BLUE)
    text.append(f"{job['name']}\n")
            
    text.append("Total time: ", style=ROBBIE_BLUE)
    text.append(f"{time.perf_counter() - start:.2f} seconds.\n")
        
    text.append("Tokens consumed: ", style=ROBBIE_BLUE)
    text.append(f"{job['tokensUsed']}\n")
        
    text.append("RESULT: ")
    if(job['status'] == "complete"):
        text.append(f"Success", style="green")
    else:
        text.append(f"{job['status']}", style="red")
                
    console.print(Panel(
        text,
        box=box.ROUNDED,
        # padding=(1, 2),
        title=Text("Run Complete", style=ROBBIE_ORANGE),
        border_style=ROBBIE_ORANGE,
    ))
    logger.debug(f"========== Run Complete ========== \n{text}")    

def print_known_error(e: RemoteCallException):
    logger.debug(e, exc_info=True)
    console.print(f"[red]An error has occurred: {e.user_friendly_message}[/red]")
    if e.additional_help:
        console.print(f"[yellow]{e.additional_help}[/yellow]")
