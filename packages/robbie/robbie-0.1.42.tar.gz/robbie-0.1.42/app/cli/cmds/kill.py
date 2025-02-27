import uuid
import typer
from rich.prompt import Confirm
from typing import Optional, List
from typing_extensions import Annotated
from common.api.list_jobs import list_jobs
from common.api.terminate_job import terminate_job
from common.api.get_job import get_job
from common.observability.main import track_command_usage
from common.console import console
from common.utils import is_valid_uuid
from cli.cmds.login import login


@track_command_usage("kill")
def kill(
  type: Annotated[str, typer.Argument(help='run')],
  ids: Annotated[List[str], typer.Argument(help="ID(s) of the run to kill")] = None,
  all: Annotated[bool, typer.Option("--all", help="Kills all runs")] = None,
  yes: Annotated[bool, typer.Option("--y", help="Skip confirmation")] = None
):
    """
    Kill a run

    Usage: robbie kill run <id> | --all

    `id` can be the positional ID returned from get runs or the UUID of the run

    """

    if type != "run":
        console.print("Please provide a valid object type to kill")
        return
    
    if ids is not None and all:
        console.print("Please provide a run ID or use --all to kill all runs")
        return
    
    login()

    # get all the jobs
    try:
        jobs = list_jobs()
        if len(jobs) == 0:
            console.print("No jobs found")
            return

        if all:
            # loop through and kill all running jobs
            if yes or Confirm.ask("[bold red]Are you sure you want to kill all runs?", default=False):
                for key, val in jobs.items():
                    if is_running(val["status"]):
                        try:
                            terminate_job(val["id"], "Killed by user CLI command")
                            console.print(f"Successfully killed run: {key}, name: {val['name']} - uuid: {val['id']}")
                        except Exception as e:
                            console.print(f"Failed to kill run: {key}, name: {val['name']} - uuid: {val['id']}, error: {e}")
            else:
                console.print("No runs were killed")
            return

        # Now figure out which type of ID we are dealing with

        # Support the ability to kill by UUID too
        for id in ids:
            if is_valid_uuid(id):
                if yes or Confirm.ask(f"[bold red]Are you sure you want to kill run:{id}?", default=False):
                    try:
                        val = get_job(id)
                        if is_running(val["status"]):
                            terminate_job(id, "Killed by using kill CLI command")
                            console.print(f"Successfully killed run: {id}, name: {val['name']} - uuid: {val['id']}")
                        else:
                            console.print(f"Sorry, run not runnning: {id}, name: {val['name']} - status: {val['status']}")
                    except Exception as e:
                        console.print(f"Failed to kill run: {id}, error: {e}")
                else:
                    console.print("Run not killed")

            # User provided a short run ID from the `robbie get runs` command
            for key, val in jobs.items():
                if key == id:
                    if yes or Confirm.ask(f"[bold red]Are you sure you want to kill run:{id}?", default=False):
                        if is_running(val["status"]):
                            try:
                                terminate_job(val["id"], "Killed by using kill CLI command")
                                console.print(f"Successfully killed run: {id}, name: {val['name']} - uuid: {val['id']}")
                            except Exception as e:
                                console.print(f"Failed to kill run: {id}, name: {val['name']} - uuid: {val['id']}, error: {e}")
                        else:
                            console.print(f"Sorry, run not runnning: {id}, name: {val['name']} - uuid: {val['id']} - status: {val['status']}")
                    else:
                        console.print("Run not killed")
        return
    except Exception as e:
        console.print(f"Failed to list jobs: {e}")
        return


def is_running(status):
    """Check if the status is running"""
    if (status != "terminated" 
        and status != "terminate_job"
        and status != "complete" 
        and status != "failed" 
        and status != "execution_error"):
        return True
    else:
        return False
    