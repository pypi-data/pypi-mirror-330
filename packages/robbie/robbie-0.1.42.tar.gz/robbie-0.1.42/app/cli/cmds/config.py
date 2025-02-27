import os
import typer
import pyfiglet
from typing_extensions import Annotated
from common.console import console
from common.constants import JOB_CONF_YAML_PATH
from common.observability.main import track_command_usage
from cli.interactive import (
    prompt_and_build_positron_job_config,
    get_job_config_yaml_name
)
from common.console import console, ROBBIE_BLUE, ROBBIE_DEFAULT


@track_command_usage("configure")
def config() -> None:
    """
    Build a Robbie job configure file (job_config.yaml) interactively.

    """
    ascii_banner = pyfiglet.figlet_format("Robbie")
    console.print(ascii_banner, style='#41a7ff')

    console.print("[green]✔[/green] Current working directory: ", os.getcwd(), style=ROBBIE_BLUE)

    console.print(f"\nPlease follow the prompts to build a job configration .yaml file ([{ROBBIE_DEFAULT}][] = default[/{ROBBIE_DEFAULT}], <tab> for menu, contol-c to exit):", style=ROBBIE_BLUE)
    
    cfg = prompt_and_build_positron_job_config(
        job_config_yaml = None,
        cmd_runner_dash_i=False,
    )

    if cfg:
        filename = get_job_config_yaml_name()
        if filename:
            cfg.write_to_file(filename=filename)
            console.print(f"[green]Successfully wrote config file {JOB_CONF_YAML_PATH}'")
            console.print("File contents:")
            with open(filename, 'r') as f:
                print(f.read())





    
