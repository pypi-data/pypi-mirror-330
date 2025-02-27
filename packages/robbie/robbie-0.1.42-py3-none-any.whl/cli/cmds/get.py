import typer
import csv
from datetime import datetime, timezone
from typing import Optional
from typing_extensions import Annotated
from common.api.list_jobs import list_jobs
from common.observability.main import track_command_usage
from common.console import console
from cli.cmds.login import login

@track_command_usage("get")
def get(
  type: Annotated[Optional[str], typer.Argument(help='runs')] = None,
  all: Annotated[bool, typer.Option("--all", help="Show runs in the running state")] = None,
  verbose: Annotated[bool, typer.Option("--v", help="Show more info about the run")] = None,
  save: Annotated[str, typer.Option("--save", help="Output the results as a .csv to <file> instead of printing")] = None
):
    """
    Get a list of "running' runs
    """

    verbose_data = [
        ["ID", "Name", "Status", "Duration (HH:MM:SS)", "Start Time (local)", "End time (local)", "Rate", "Tokens Used", "UUID"],
        ["--", "----", "------", "-------------------", "------------------", "----------------", "----", "-----------", "----"],
    ]

    simple_data = [
        ["ID", "Name", "Status", "Rate", "Tokens Used" ],
        ["--", "----", "------", "----", "-----------" ],
    ]
    
    '''
    console.print(f"===== get =====")
    console.print(f"type: {type}")
    console.print(f"all: {all}")
    console.print(f"verbose: {verbose}")
    console.print(f"save: {save}")
    '''

    login()

    if type == "runs":
        try:
            jobs = list_jobs()
            if len(jobs) == 0:
                console.print("No runs found")
                return

            for key, val in jobs.items():
                if not is_running(val["status"]) and not all:
                    continue
                duration = convert_ms(val['durationMs']) if val['durationMs'] != None else None
                local_start_time = convert_utc_to_local(val['startDate']) if val['startDate'] != None else None
                local_end_time = convert_utc_to_local(val['endDate']) if val['endDate'] != None else None

                if verbose:
                    verbose_data.append([key, val['name'], val['status'], duration, local_start_time, local_end_time, val['startTokenRate'], val['tokensUsed'], val['id']])    
                else:   
                    simple_data.append([key, val['name'], val['status'], val['startTokenRate'], val['tokensUsed']])

            if save:
                # we are writing to a file
                if verbose:
                    if not save.endswith(".csv"):
                        save += ".csv"
                    with open(save, "w", newline="") as file:
                        try:
                            writer = csv.writer(file)
                            writer.writerows(verbose_data)
                            console.print(f"[green]Successfully wrote file:{save}[/green]")
                        except Exception as e:
                            console.print(f"[red]Error writing to file:{save} error: {e}[/red]")
                else:
                    if not save.endswith(".csv"):
                        save += ".csv"
                    with open(save, "w", newline="") as file:
                        try:
                            writer = csv.writer(file)
                            writer.writerows(simple_data)
                            console.print(f"[green]Successfully wrote file:{save}[/green]")
                        except Exception as e:
                            console.print(f"[red]Error writing to file:{save} error: {e}[/red]")
            else:
                # we are printing
                if verbose:
                    col_widths = [max(len(str(row[i])) for row in verbose_data) for i in range(len(verbose_data[0]))]
                    for row in verbose_data:
                        console.print("  ".join(f"{str(item):<{width}}" for item, width in zip(row, col_widths)))
                else:
                    col_widths = [max(len(str(row[i])) for row in simple_data) for i in range(len(simple_data[0]))]
                    for row in simple_data:
                        console.print("  ".join(f"{str(item):<{width}}" for item, width in zip(row, col_widths)))
        except Exception as e:
            console.print(f"[red]Error getting runs: {e}[/red]")
    else:    
        console.print("[red]Please provide a valid type, like 'runs'[/red]")

def convert_ms(ms):
    """Converts milliseconds to hours, minutes, and seconds."""
    seconds, ms = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def convert_utc_to_local(utc_time_str):
    """Converts a UTC time string to a local time string."""
    # Parse the UTC time string to a datetime object
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Set the datetime object to UTC timezone
    utc_time = utc_time.replace(tzinfo=timezone.utc)

    # Convert UTC time to local time
    local_time = utc_time.astimezone()

    # Format the local time as a string
    local_time_str = local_time.strftime("%Y-%m-%d %H:%M:%S")

    return local_time_str


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
           