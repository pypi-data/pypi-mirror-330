import requests
import os
import typer
import re
from typing_extensions import Annotated
from typing import Optional
from tqdm.auto import tqdm
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator
from common.api.list_jobs import list_jobs
from common.api.get_job import get_job
from common.api.presigned_url import get_download_presigned_url
from common.exceptions import RobbieException, RemoteCallException
from common.console import console, ROBBIE_BLUE
from common.logging_config import logger
from common.observability.main import track_command_usage
from common.utils import is_valid_uuid
from cli.auto_complete import jobs_auto_complete


COMPRESSED_RESULTS = 'result.zip'

@track_command_usage("download")
def download(
    job_id_arg: Annotated[Optional[str], typer.Option("--run", 
                                                      help='Run UUID',
                                                      autocompletion=jobs_auto_complete)] = None,
    filename: Annotated[Optional[str], typer.Option("--filename", help='Name of the file to download or all for a tar file of all results.')] = None,
    local_path: Annotated[Optional[str], typer.Option("--path", help='Path of where to download the file.')] = ".",
) -> None:
    """
        Download command for Robbie CLI - allows users to download result.zip from a job.
        
        Prompts the user to choose a job to download results from.
    """
    try:
        if not filename_is_valid(filename):
            console.print('[red]Error: Please specify a valid file name or "all" to download all files.')
            return
        
        if local_path and not os.path.exists(local_path):
            console.print('[red]Error: The path you specified is not valid.')
            return

        if job_id_arg:
            if is_valid_uuid(job_id_arg):
                download_chosen_results(job_id_arg, filename, local_path)
            else:
                console.print("[red]Error: Please enter a valid run id in UUID format.")
        else:
            # prompt for the job to download
            jobs = Jobs.load()
            if jobs == None:
                 console.print('[red]Error: No jobs')
                 return
            
            def is_job_valid(text):
                return text == "" or text in jobs.menu_items()
            job_validator = Validator.from_callable(is_job_valid, error_message='Please enter a valid run name.')

            jobs_choice = prompt('Choose a run to download: <tab for menu>: ', completer=WordCompleter(jobs.menu_items()), validator=job_validator)
            if jobs_choice == "" or jobs_choice == None:
                console.print("No job selected. Exiting.")
                return
            download_chosen_results(jobs.id_from_menu_item(jobs_choice), filename, local_path)
    except RobbieException as e:
        console.print(f"[red]Error: {e}[/red]")
    except RemoteCallException as e:
        console.print(f"[red]Error: {e}[/red]")
    
def filename_is_valid(filename: str) -> bool:
    """Check if the download argument is valid."""
    if filename == None:
        return False
    if filename == "all":
        return True
    if filename == "":
        return False
    return True

def sanitize_file_name(file_name: str) -> str:
    """
    Replace invalid characters in file names with an underscore.
    """
    # Replace invalid Windows characters with '_'
    return re.sub(r'[<>:"/\\|?*]', '_', file_name)

def download_chosen_results(job_id: str, filename: str, local_path: str):
    """The user can download a single file or all files from the run."""
    if filename == "all":
        download_tar_results_file(job_id, local_path)
    elif filename == None or filename == "":
        raise RobbieException(f"Nothing to download run {job_id}")
    else:
        download_individual_results_file(job_id, filename, local_path)

def download_tar_results_file(job_id: str, local_path: str = "."):
    """
    Download the result.zip file from the job and stores it in the CWD

    Raises:
        RobbieException: If we can't generate a presigned URL or downloading fails
    """
    job = get_job(job_id)
    if(job == None):
        raise RobbieException(f"No such run: {job_id}")

    if(job["resultsPresignedBucketInfo"] == None):
        raise RobbieException(f"No resultsPresignedBucketInfo for job {job_id}")

    logger.debug("resultsPresignedBucketInfo", job["resultsPresignedBucketInfo"])

    logger.debug(f'Downloading results for: {job["name"]}')

    response = requests.get(job["resultsPresignedBucketInfo"],stream=True) 
    if response.status_code != 200:
        logger.debug(f'Failed to download URL, http code: {response.status_code} \n {response.text}')
        raise RobbieException('Sorry, run has no results to download.') 
    else:
        # Sizes in bytes.
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024

        console.print(f'Download results for: {job["name"]}')

        # handles the case when None is explicitly passed by deploy.py
        if local_path == None:
            open_path = f"./{COMPRESSED_RESULTS}"
        else:
            open_path = f"{local_path}/{COMPRESSED_RESULTS}"

        console.print(f"Downloading file: {COMPRESSED_RESULTS} for run {job_id}, to {open_path}")
        with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
            with open(open_path, "wb") as file:
                logger.debug(f'Successfully opened: {open_path}')
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)

        if total_size != 0 and progress_bar.n != total_size:
            raise RobbieException(f'failed to download file')
    
        console.print("[green]✔[/green] Results now available.")


def download_individual_results_file(job_id: str, file_name: str, local_path: str = "."):
    """
    Download a single file from the job and stores it in the CWD

    Raises:
        RobbieException: If we can't generate a presigned URL or downloading fails
    """
    
    file_url = get_download_presigned_url(job_id, f"result/{file_name}")
    if(file_url == None):
        raise RobbieException(f"No such file: {file_name} for run {job_id}")

    logger.debug(f"file_url: {file_url}")
    logger.debug(f"Downloading file: {file_name} for run {job_id}")

    # Sanitize file name for Windows compatibility
    sanitized_file_name = sanitize_file_name(file_name)
    logger.debug(f"Sanitized file name: {sanitized_file_name}")

    # _get_download_presigned_url returns a dict with a 'url' key
    response = requests.get(file_url['url'], stream=True) 
    if response.status_code != 200:
        logger.debug(f'Failed to download URL, http code: {response.status_code} \n {response.text}')
        raise RobbieException(f'Sorry, {file_name} does not exist for run: {job_id}.') 
    else:
        # Sizes in bytes.
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024

        # handles the case when None is explicitly passed by deploy.py
        if local_path is None:
            open_path = f"./{sanitized_file_name}"
        else:
            open_path = f"{local_path}/{sanitized_file_name}"

        console.print(f"Downloading file: {file_name} for run {job_id}, to {open_path}")
        with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
            with open(open_path, "wb") as file:
                logger.debug(f'Successfully opened: {open_path}')
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)

        if total_size != 0 and progress_bar.n != total_size:
            raise RobbieException(f'failed to download file: {open_path}')
        
        '''
        # perserving this code if we decide to change the functionality back to auto decompress .zip files

        _unzip(zip_file="./result.zip", path=".")
        os.remove("./result.zip")
        '''
    
        console.print("[green]✔[/green] File downloaded successfully.")

'''
# perserving this function is we decide to change the functionality back to auto decompress .zip files
def _unzip(zip_file, path):
    """
    Extracts `zip_file` and puts the `members` to `path`.
    If members is None, all members on `zip_file` will be extracted.
    """
    tree = Tree("Remote files copied to Local Machine")

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        for member in zip_ref.namelist():
            zip_ref.extract(member, path=path)
            tree.add(f"[yellow]{member}, size: {os.path.getsize(member)} bytes[/yellow]")
    console.print(tree)
'''


# Naming
JOB_ID="id"
JOB_NAME="name"
JOB_MENU="menu"

# singleton builds a list of tuples from the DB results
class Jobs: 
    is_init: bool = False
    my_jobs: dict

    def __init__(self, jobs_arg: dict):
        if self.is_init:
            raise ValueError('Jobs.load() already initialized')
        else:
            self.init = True
            self.my_jobs= jobs_arg

    @staticmethod
    def load():
        jobs = list_jobs()
        if len(jobs) == 0:
            return None
        # Loop through and add a custom "menu" item to each dict (but only if the job actually ran)
        for _, val in jobs.items(): 
            if val["durationMs"] != None:
                val[JOB_MENU] = f'{val[JOB_NAME]} (uuid: {val[JOB_ID]} )'
        return Jobs(jobs)
        
    # Prompt toolkit needs a list of strings to display in the menu 
    def menu_items(self) -> list: 
        ret_list: list = []
        for _, val in self.my_jobs.items():
            # just show names
            if val["durationMs"] != None:
                ret_list.append(val[JOB_MENU])
        return ret_list
    
    def auto_complete_items(self) -> list: 
        ret_list: list = []
        for key, val in self.my_jobs.items():
            # just show names
            if val["durationMs"] != None:
                ret_list.append((val[JOB_ID], val[JOB_NAME]))
        return ret_list
    
    def id_from_menu_item(self, menu_item: str) -> str:
        for _, val in self.my_jobs.items():
            if val["durationMs"] != None and val[JOB_MENU] == menu_item:
                return val[JOB_ID]
        return None