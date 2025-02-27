import zipfile
import os
import shutil
import fnmatch
from dataclasses import dataclass
from typing import List
from common.constants import FILE_SIZE_THRESHOLD
from positron_job_runner.runner_env import runner_env
from positron_job_runner.cloud_storage import cloud_storage
from positron_job_runner.cloud_logger import logger


EXCLUDED_DIRECTORIES = ['venv', '.venv', '.git', '__pycache__', 'job-execution', '.robbie', '.ipynb_checkpoints', 'persistent-disk']
S3_BASE_PATH = f"{runner_env.JOB_OWNER_EMAIL}/{runner_env.JOB_ID}"
S3_RESULT_PATH = f"{S3_BASE_PATH}/result"

def download_workspace_from_s3():
    """Download the workspace from S3"""
    s3_key = f"{S3_BASE_PATH}/workspace.zip"
    local_zip_path = os.path.join(runner_env.RUNNER_CWD, 'workspace.zip')
    cloud_storage.download_file(s3_key, local_zip_path)
    # the file may or may not exist

def copy_workspace_to_job_execution():
    """Copies the workspace from job-controller to job-execution"""
    local_zip_path = os.path.join(runner_env.RUNNER_CWD, 'workspace.zip')
    if os.path.exists(local_zip_path):
        destination_zip_path = os.path.join(runner_env.JOB_CWD, 'workspace.zip')
        print(f"Copying: {local_zip_path} to {destination_zip_path}")
        shutil.copy(local_zip_path, destination_zip_path)
        logger.debug(f"Copied workspace.zip to {destination_zip_path}")
    else:
        logger.error("Workspace zip not found")

def upload_results_to_s3():
    """Uploads the results to S3"""
    try:
        logger.info('Copying results to cloud storage...')

        results_dir = runner_env.JOB_CWD
        os.makedirs(results_dir, exist_ok=True)

        result_files = get_file_paths(path=results_dir, excluded_dirs=EXCLUDED_DIRECTORIES)

        ignore_name_patterns = []
        # read in the ignore file
        for entry in result_files:
            if ".robbieignore" == entry.name:
                with open(entry.full_path, "r") as f:
                    ignore_name_patterns = f.read().splitlines()

        # Create a zip of the result directory
        results_zip_file_name = f"{results_dir}/result.zip"
        with zipfile.ZipFile(results_zip_file_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in result_files:
                ignore = False
                for pattern in ignore_name_patterns:
                    if fnmatch.fnmatch(file.name, pattern):
                        logger.debug(f"Ignoring: {file.name}")
                        ignore = True
                        break
                if not ignore:
                    logger.debug(f"Adding to zip: {file.name}")
                    zipf.write(file.full_path, arcname=file.name)

        file_size = os.path.getsize(results_zip_file_name)
        if (file_size >= FILE_SIZE_THRESHOLD):
            size_in_mb = round(file_size / (1024 * 1024), 2)
            logger.warning(f"Results Archive Size: {size_in_mb} Mb. It might take a long time to upload it.")

        logger.debug(f"Uploading to cloud storage: {results_zip_file_name}")
        cloud_storage.upload_file(results_zip_file_name, f"{S3_RESULT_PATH}/result.zip")

        # Upload raw files to S3
        for file in result_files:
            logger.debug(f"Uploading to cloud storage: {file.name}")
            s3_key = f"{S3_RESULT_PATH}/{file.name}"
            cloud_storage.upload_file(file.full_path, s3_key)

        logger.info('Results uploaded to S3 successfully')

    except Exception as e:
        logger.error(f"Failed to upload results to S3: {e}")


@dataclass
class FileEntry:
    full_path: str
    name: str
    size: int

def get_file_paths(path: str, excluded_dirs: List[str], excluded_files: List[str] = []) -> List[FileEntry]:
    """should return a list relative paths that should included in the results"""
    all_files: List[FileEntry] = []
    for root, dirs, files in os.walk(path):
        for exclude_dir in excluded_dirs:
            try:
                dirs.remove(exclude_dir)
            except ValueError:
                pass
        for file in files:
            if file in excluded_files:
                continue
            full_path = os.path.join(root, file)
            file_size = os.path.getsize(full_path)
            rel_path = os.path.relpath(full_path, path)
            all_files.append(FileEntry(name=rel_path, size=file_size, full_path=full_path))
    return all_files


