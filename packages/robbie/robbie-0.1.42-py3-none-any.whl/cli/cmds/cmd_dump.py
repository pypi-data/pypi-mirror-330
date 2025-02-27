import typer
import pyfiglet
from typing import Optional
from typing_extensions import Annotated
from common.common_dump import common_dump
from common.observability.main import track_command_usage
from common.env_defaults import current
from common.console import console

# robbie "dump" command
# @track_command_usage("dump")
def dump(
    machine: Annotated[bool, typer.Option("--machine", help="Machine related info on the local machine")] = None,
    conda: Annotated[bool, typer.Option("--conda", help='Conda related parameters on the local machine')] = None,
    python: Annotated[bool, typer.Option("--python", help="Python related info on the local machine")] = None,
    sdk: Annotated[bool, typer.Option("--sdk", help="Robbie SDK related configuration")] = None,
    job_config: Annotated[bool, typer.Option("--job_config", help="Job related configuration")] = None,
    job_config_name: Annotated[Optional[str], typer.Argument()] = None,
    save: Annotated[str, typer.Option("--save", help="Saves configuration info to a file that can be emailed.")] = None 
):

    ascii_banner = pyfiglet.figlet_format(f"Robbie - {current.name}")
    console.print(ascii_banner, style='#41a7ff')

    common_dump(
        machine,
        conda,
        python,
        sdk,
        (True if job_config else False),
        (job_config_name if job_config_name else None),
        save
    )
