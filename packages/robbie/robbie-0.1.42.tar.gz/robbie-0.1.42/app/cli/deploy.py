import time
import signal
import threading
from rich.prompt import Confirm
from common.exceptions import RemoteCallException
from common.custom_file_filter import (
    CustomFileFilter,
    copy_workdir
)
from common.env_config import env
from common.config import PositronJob
from common.cli_args import args as cli_args
from common.print_banner import *
from common.console import console, ROBBIE_BLUE
from cli.cmds.download import download_chosen_results
from common.job import _prepare_and_upload_workspace
from common.logging_config import logger
import common.api.stream_logs
from common.api.get_job import get_job, get_job_status
from common.api.start_job import start_job
from common.api.terminate_job import terminate_job
from common.api.create_job import create_job
from common.utils import _exit_by_mode, SUCCESS, FAILURE
from common.validation import warn_python_version
from common.local_container import run_local_docker_container

# number of seconds to poll when monitoring job status
POLLING_SEC=1

# for the the deep link
PORTAL_BASE = env.API_BASE.rstrip('/api')
    
def command_runner_deploy(job_config: PositronJob):
    """
    This function is the entry point for the running a command on a remote machine.
    It can be called in two ways:
    - Mode 1 - From the command line with the `positron run` command
    - Mode 2 - From the run_notebook() function when running in a notebook (Jupyter, Colab, VScode
    """
    
    try:
        logger.debug(job_config.to_string("command_runner_deploy"))
        job_config.validate_values()
        
        warn_python_version(job_config.image)

        # TODO: We should not be creating a job before we let the user run it, we need defaults in the DBs that we can query
        logger.debug(job_config.create_runtime_env())
        job = create_job(job_config=job_config)

        # we want to print out the files that will be copied over
        if job_config.custom_file_filter:
            custom_file_filter = CustomFileFilter(ignore_name_patterns=job_config.custom_file_filter)
        else:
            custom_file_filter = None
        
        # this just builds the tree so we can print it out
        # actual files are copied later
        copy_workdir(".", custom_file_filter, print_tree=True)

        print_robbie_configuration_banner(job, job_config)

        # prompt the user if they don't pass the -y option
        if not cli_args.skip_prompts:
            if not Confirm.ask("Run with these settings?", default=True):
                terminate_job(job["id"], "User declined from CLI")
                console.print("[yellow]See you soon![/yellow]")
                return

        # tell people we are on the local machine
        console.print("[bold]Local Machine: [/bold]", style=ROBBIE_BLUE)    

        console.print("[green]✔[/green] [1/3] Packaged up workspace artifacts.", style=ROBBIE_BLUE)

        _prepare_and_upload_workspace(
            job_id = job['id'], 
            local_deps_path = job_config.dependencies,
            include_local_workdir = True if job_config.include_local_dir else False,
            pre_execution_commands = None,
            pre_execution_script_local_path = None,
            custom_file_filter = custom_file_filter,
        )
        console.print("[green]✔[/green] [2/3] Uploaded compressed workspace to Robbie.", style=ROBBIE_BLUE)
        
        if cli_args.create_only:
            console.print(f"[green]✔[/green] [3/3] Job created successfully", style=ROBBIE_BLUE)
            console.print(f"JOB_ID: {job.get('id')}")
            if cli_args.local_container:
                run_local_docker_container(job.get('id'), cli_args.local_container)
            return

        # start the job up
        start_job(job_id=job['id'], data=job_config.create_runtime_env())
        console.print("[green]✔[/green] [3/3] Submitted job to Robbie.", style=ROBBIE_BLUE)

        start = time.perf_counter()
        print_job_details_banner(job)
        console.print(f"You can also monitor job status in the Robbie portal at: {PORTAL_BASE}/portal/app/my-runs?jobId={job['id']}\n", style=ROBBIE_BLUE) 

        # Are we streaming stdout or just showing the status changes.
        if cli_args.stream_stdout:
            # tell people we are on the remote machine
            console.print("[bold]Remote Machine Status: [/bold]", style=ROBBIE_BLUE)  

            thread = threading.Thread(target=print_job_status, args=(job,))
            thread.start()

            common.api.stream_logs.start_stdout_stream(job['id'], job_config.verbose)
            
            thread.join()

            final_get_job = get_job(job['id'])
            # did someone interrupt the stream?
            if _is_job_done(final_get_job):
                print_job_complete_banner(final_get_job, start)
                if cli_args.download:
                    # download the results
                    download_chosen_results(final_get_job['id'], cli_args.download, cli_args.local_path)
            
                if _was_job_a_success(final_get_job):
                    _exit_by_mode(SUCCESS)
                else:
                    _exit_by_mode(FAILURE)
            else:
                console.print(f"You can monitor job status in the Robbie portal at: {PORTAL_BASE}/portal/app/my-runs?jobId={job['id']}", style=ROBBIE_BLUE) 
                _exit_by_mode(SUCCESS)
    
    except KeyboardInterrupt:
        if Confirm.ask("Interrupt received, do you want to terminate the run?", default=False):
            console.print("[yellow]Terminating run...[/yellow]")
            if job is not None:
                terminate_job(job['id'], "User interrupted")
            # the CLI will exit when the main loop sees the status change.
        else:
            console.print("[yellow]Exiting...run will continue. Please monitor in the portal.[/yellow]")
            _exit_by_mode(SUCCESS)
    except RemoteCallException as e:
        """For known errors we dont print exceptions, we just print the user friendly message"""
        print_known_error(e)
        _exit_by_mode(FAILURE)
    except Exception as e:
        # don't let this propagate up, we want to catch all exceptions
        logger.exception(e)
        print(e)
        _exit_by_mode(FAILURE)

def _is_job_done(job) -> bool:
    return (
        job['status'] == "terminated" or 
        job['status'] == "complete" or 
        job['status'] == "failed" or 
        job['status'] == "execution_error" or
        job['status'] == "terminate_job"
    )

def _was_job_a_success(job) -> bool:
    return job['status'] == "complete"

def print_job_status(job):
    """
    Print the job status to the console
    """
    last_status_change = "Starting..."
    start_time = time.time()

    console.print("Processing...", style=ROBBIE_BLUE)   

    try:
        while True:
            job = get_job_status(job['id'])
            # are we in a final state?
            # print("job status: ", job['status'], "is_set: ", common.api.stream_logs.stop_flag.is_set())
            if(_is_job_done(job) or common.api.stream_logs.stop_flag.is_set()):
                break

            # there has been a status change
            if(job['status'] != last_status_change):
                # take care of the previous status
                if last_status_change != "Starting...":
                    elapsed_time = time.time() - start_time
                    minutes = int(elapsed_time // 60)
                    seconds = int(elapsed_time % 60)
                    tenth_of_seconds = int((elapsed_time * 10) % 10)
                    if minutes > 0:
                        timer_text = "{:3}m {:2}.{:1}s".format(minutes, seconds, tenth_of_seconds)
                    else:
                        timer_text = "{:2}.{:1}s".format(seconds, tenth_of_seconds)
                    console.print(timer_text)

                # print out the new job status
                # print out the new job status
                if job['status'] == "started_container":
                    console.print(f" => booting_runtime...", end="")
                else:
                    console.print(f" => {job['status']}...", end="")
                last_status_change = job['status']
                start_time = time.time()
            time.sleep(POLLING_SEC)

    except Exception as e:
        console.print(f"print_job_status error: {e}")  
    finally:
        logger.debug("Done monitoring status...")