import os
import signal
import json
import time
import sentry_sdk
import secrets
import threading
from rich.prompt import Confirm
from remote_function.stored_function import StoredFunction
from common.validation import validate_python_version
from common.utils import _exit_by_mode, SUCCESS, FAILURE, _nb
from common.exceptions import RemoteFunctionException, RemoteCallException
from common.custom_file_filter import (
    CustomFileFilter,
    copy_workdir
)

import common.api.stream_logs
from common.config import PositronJob
from common.enums import JobStatus, failed_job_statuses
from common.api.stream_logs import start_stdout_stream
from common.api.get_job import get_job_status, get_job
from common.api.start_job import start_job
from common.api.terminate_job import terminate_job
from common.api.create_job import create_job
from common.cli_args import args as cli_args
from common.job import _prepare_and_upload_workspace
from common.env_config import env
from common.user_config import user_config
from common.console import console, ROBBIE_BLUE
from common.logging_config import logger
from common.api.terminate_job import terminate_job
from common.print_banner import (
    print_robbie_configuration_banner, 
    print_job_details_banner, 
    print_known_error, 
    print_job_complete_banner
)

from common.local_container import run_local_docker_container

# TODO: update env var to just be base url
PORTAL_BASE = env.API_BASE.rstrip('/api')

# number of seconds to poll when monitoring job status
POLLING_SEC=1

class Deploy:
    @staticmethod
    def remote_function_deploy(func, args, kwargs, job_config: PositronJob):
        global job
        # signal.signal(signal.SIGINT, handle_sigint)
        try:
            # TODO: lots of this code is the same as the other `deploy` file, need to consolidate
            logger.debug(f'Job Config: {job_config}')
            job_config.validate_values()
            logger.debug(f'Runtime Environment: {job_config.create_runtime_env()}')

            if not validate_python_version(job_config.image):
                _exit_by_mode(FAILURE)
                return

            job = create_job(job_config)

            if job_config.custom_file_filter:
                custom_file_filter = CustomFileFilter(ignore_name_patterns=job_config.custom_file_filter)
            else:
                custom_file_filter = None

            # this just builds the tree so we can print it out
             # actual files are copied later
            copy_workdir(".", custom_file_filter, print_tree=True)

            print_robbie_configuration_banner(job, job_config)
            logger.debug(f"Created Run Details: {json.dumps(job, indent=2)}")

            # prompt the user if they don't pass the -y option
            if not cli_args.skip_prompts:
                user_input = input("Run with these settings? (Y/n)")
                if not user_input.lower() in ["", "yes", "y", "Yes", "Y"]:
                    terminate_job(job["id"], "User declined from CLI")
                    console.print("[yellow]See you soon![/yellow]")
                    return

            console.print("\n[bold]Local Machine: [/bold]", style=ROBBIE_BLUE)    

            # create a random key for the function integrity check
            hmac_key = secrets.token_hex(32)
            # hack to get the secret key into the environment when running a local container
            os.environ['REMOTE_FUNCTION_SECRET_KEY'] = hmac_key

            console.print("[green]✔[/green] [1/4] Serialized function.", style=ROBBIE_BLUE)
            # Create stored function from func and arguments
            stored_function = StoredFunction(func, args, kwargs)
            stored_function.set_job_id(job['id'])
            stored_function.serialize_function()
            logger.debug(f"### create_function_metadata(): user_config.user_auth_token = {user_config.user_auth_token}")
            stored_function.create_function_metadata(hmac_key=hmac_key)
            stored_function.upload_to_s3()

            console.print("[green]✔[/green] [2/4] Packaged up workspace artifacts.", style=ROBBIE_BLUE)
        
            # now upload workspace (current directory and deps)
            _prepare_and_upload_workspace(
                job_id = job['id'], 
                local_deps_path = job_config.dependencies,
                include_local_workdir = True if job_config.include_local_dir else False,
                pre_execution_commands = None,
                pre_execution_script_local_path = None,
                # custom_file_filter = None,
                custom_file_filter = custom_file_filter
            )
            console.print("[green]✔[/green] [3/4] Uploaded compressed workspace to Robbie.", style=ROBBIE_BLUE)

            if cli_args.create_only:
                console.print(f"[green]✔[/green] [4/4] Run created successfully.")
                console.print(f"JOB_ID: {job.get('id')}")
                if cli_args.local_container:
                    run_local_docker_container(job.get('id'), cli_args.local_container)
                _exit_by_mode(SUCCESS)
                return

            # set the secret key
            runtime_env = job_config.create_runtime_env()
            runtime_env['REMOTE_FUNCTION_SECRET_KEY'] = hmac_key
            
            logger.debug(f"Runtime Environment: {runtime_env}")
             # start job
            start_job(job_id=job['id'], data=runtime_env)
            console.print("[green]✔[/green] [4/4] Submitted run to Robbie.", style=ROBBIE_BLUE)
            
            start = time.perf_counter()
            print_job_details_banner(job)
            console.print(f"You can also monitor run status in the Robbie portal at: {PORTAL_BASE}/portal/app/my-runs?jobId={job['id']}\n", style=ROBBIE_BLUE)

            # Start standard output stream if option selected
            console.print("Waiting for remote job to finish...", style=ROBBIE_BLUE)

            if cli_args.stream_stdout:
                thread = threading.Thread(target=print_job_status, args=(job,))
                # job status printing thread
                thread.start()
                # start the stdout stream
                common.api.stream_logs.start_stdout_stream(job['id'], job_config.verbose)
                thread.join()

            while True:
                job = get_job_status(job['id'])
                if job['status'] == JobStatus.complete:
                    console.print(f"[green]✔[/green] Done! Now processing results...")
                    result, exception = stored_function.load_and_validate_results(hmac_key=hmac_key)
                    console.print("Passing back result.")
                    if exception is not None:
                        raise RemoteFunctionException(exception)
                    else:
                        return result
                elif job['status'] == JobStatus.failed or job['status'] == JobStatus.execution_error:
                    raise RemoteCallException(user_friendly_message="The remote run has failed, please check job output logs for further details!")
                elif job['status'] == JobStatus.terminated:
                    # users terminated
                    break
                elif job['status'] == JobStatus.terminate:
                    # we terminated
                    break
                time.sleep(2)

            # get the job info a final time
            job = get_job(job['id'])
            print_job_complete_banner(job, start)
            # print details if error for debugging.
            if job['status'] in failed_job_statuses:
                console.print(f"We are sorry that your job has run in to an issue. If you continue to have issues, please contact support@robbie.run and provide the following traceback.\nTrace ID: {sentry_sdk.get_current_span().trace_id}")
            _exit_by_mode(SUCCESS)

        except KeyboardInterrupt:
            if Confirm.ask("Interrupt received, do you want to terminate the run?", default=False):
                console.print("[yellow]Terminating run...[/yellow]")
                terminate_job(job['id'], "User interrupted")
            
        except RemoteCallException as e:
            """For known errors we dont print exceptions, we just print the user friendly message"""
            print_known_error(e)
            _exit_by_mode(FAILURE)
        except RemoteFunctionException as e:
            """
                When the result of a remote function call is an Exception being raised
                this is how we let the deserialized exception bubble up back to the client side
            """
            raise e.rf_exception
        except Exception:
            console.print_exception()


def _is_job_done(job) -> bool:
    return (
        job['status'] == "terminated" or 
        job['status'] == "complete" or 
        job['status'] == "failed" or 
        job['status'] == "execution_error" or
        job['status'] == "terminate_job"
    )

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
