import uuid
import typer
from rich.prompt import Confirm
from typing import Optional
from typing_extensions import Annotated
from common.api.list_jobs import list_jobs
from common.api.delete_job import delete_job
from common.api.get_job import get_job
from common.observability.main import track_command_usage
from common.console import console
from common.utils import is_valid_uuid
from cli.cmds.login import login


@track_command_usage("delete")
def delete(
  type: Annotated[str, typer.Argument(help='run')],
  id: Annotated[Optional[str], typer.Argument(help="ID of the run to delete")] = None,
  all: Annotated[Optional[bool], typer.Option("--all", help="Delete all runs")] = None,
  yes: Annotated[Optional[bool], typer.Option("--y", help="Skip confirmation")] = None
):
    """
    Delete a run artifacts

    Usage: robbie delete run <id> | --all

    `id` can be the positional ID returned from get runs or the UUID of the run

    """

    if type != "run":
        console.print("Please provide a valid object type to delete")
        return
    
    if id is not None and all:
        console.print("Please provide a run ID or use --all to delete all runs")
        return
    
    login()

    try:
        # get all the jobs  
        jobs = list_jobs()
        if len(jobs) == 0:
            console.print("No jobs found")
            return

        if all:
            # loop through and delete all runs
            if yes or Confirm.ask("[bold red]Are you sure you want to delete all runs?", default=False):
                for key, val in jobs.items():
                    try:
                        delete_job(val["id"])
                        console.print(f"Successfully deleted run: {key}, name: {val['name']} - uuid: {val['id']}")
                    except Exception as e:
                        console.print(f"Failed to delete run: {key}, name: {val['name']} - uuid: {val['id']}, error: {e}")
            else:
                console.print("No runs were deleted")
            return

        # Now figure out which type of ID we are dealing with

        # Support the ability to kill by UUID too
        if is_valid_uuid(id):
            if yes or Confirm.ask(f"[bold red]Are you sure you want to delete run:{id}?", default=False):
                try:
                    val = get_job(id)
                    delete_job(id)
                    console.print(f"Successfully deleted run: {id}, name: {val['name']} - uuid: {val['id']}")
                    return
                except Exception as e:
                    console.print(f"Failed to delete run: {id}, error: {e}")
                    return
            else:
                console.print("Run not deleted")
                return

        # User provided a short run ID from the `robbie get runs` command
        for key, val in jobs.items():
            if key == id:
                if yes or Confirm.ask(f"[bold red]Are you sure you want to delete run:{id}?", default=False):
                    try:
                        delete_job(val["id"])
                        console.print(f"Successfully deleted run: {id}, name: {val['name']} - uuid: {val['id']}")
                        return
                    except Exception as e:
                        console.print(f"Failed to delete run: {id}, name: {val['name']} - uuid: {val['id']}, error: {e}")
                        return
                else:
                    console.print("Run not deleted")
                    return

        console.print(f"Run {id} not found")
        return
    except Exception as e:
        console.print(f"Error deleting run: {id}, error: {e}")
        return
    