import asyncio
import socketio
import nest_asyncio
import json
import time
import threading
from rich.prompt import Confirm
from common.env_config import env
from common.exceptions import RobbieException
from common.api.terminate_job import terminate_job
from ..console import console, ROBBIE_BLUE
from ..logging_config import logger
from common.cli_args import args as cli_args

my_job_id = None
verbose_logging = False
stop_flag = None

sio = socketio.AsyncClient(ssl_verify=False)
nest_asyncio.apply() # enabled nested event loops

@sio.event(namespace='/stdout-stream')
async def connect():
    # console.print("Connected to your run's log stream!")
    logger.debug("Connected to the log stream")

@sio.event(namespace='/stdout-stream')
async def message(message: str):
    # print(f"logging received message, verbose: {verbose_logging}: {message}")
    try:
        log: dict = json.loads(message)
        level_name = log.get('log_level')
        # timestamp = time.strftime("%H:%M:%S", time.gmtime(log.get('timestamp') / 1000))
        timestamp = time.strftime("%H:%M:%S")
        message = log.get('message')
        level_string = level_name.ljust(8)
        logger_name = log.get('app_name')

        if level_name == "INFO":
            level_string = f"[green]{level_name}[/green]"
        elif level_name == "DEBUG":
            level_string = f"[blue]{level_name}[/blue]"
        elif level_name == "ERROR":
            level_string = f"[red]{level_name}[/red]"
        elif level_name == "WARNING":
            level_string = f"[yellow]{level_name}[/yellow]"

        if verbose_logging:
            formatted_log = f" => => {timestamp} {level_string}: {message}"
            console.print(formatted_log)
        else:
            # only print the job-related logs
            if "job stderr:" in message:
                formatted_log = f" => => {message.lstrip('job stderr:')}"
            if "job stdout:" in message:
                formatted_log = f" => => {message.lstrip('job stdout:')}"
            if "job stderr" in message or "job stdout" in message:
                console.print(formatted_log)
    except Exception as error:
        print(f"Error parsing log message: {error}")
        console.print(log['message'], style=ROBBIE_BLUE)

@sio.event(namespace='/stdout-stream')
async def disconnect():
    print("Disconnected from the log stream")
    logger.debug("Disconnecting from the log stream")
    stop_flag.set()

@sio.event(namespace='/stdout-stream')
async def error(err):
    console.print('An error occurred in the streaming process')
    logger.error(err)

async def start_stream(job_id: str):
    global my_job_id

    custom_headers = {
        "PositronAuthToken": env.USER_AUTH_TOKEN,
        "PositronJobId": job_id
    }
    await sio.connect(env.SOCKET_IO_DOMAIN, headers=custom_headers, socketio_path=env.SOCKET_IO_PATH)
    # TODO: I don't think we want to actually do this long term.
    try:
        await sio.wait()
    except asyncio.exceptions.CancelledError as error:
        # keyboard interrupt
        if my_job_id:
            if Confirm.ask("Interrupt received, do you want to terminate the run?", default=False):
                console.print("[yellow]Terminating run...[/yellow]")
                terminate_job(my_job_id, "User interrupted")
                # kind of a kluge, but we need to set this to false so it doesn't download results
                cli_args.download = False
                global stop_flag
                stop_flag.set()
            else:
                console.print("[yellow]Streaming ended. Please monitor run progress in the portal.[/yellow]")  
    except Exception as error:
        print(f"Error in start_stream: {error}")
    finally:
        logger.debug("Done waiting...")

def start_stdout_stream(job_id: str, verbose: bool = False):
    global my_job_id
    global verbose_logging
    global stop_flag

    my_job_id = job_id 
    verbose_logging = verbose
    # this is so the background thread can stop when the main thread gets a keyboard interrupt
    stop_flag = threading.Event()    

    try:
        # Start the stream
        asyncio.get_event_loop().run_until_complete(start_stream(job_id))
    except Exception as error:
        raise RobbieException(error)


