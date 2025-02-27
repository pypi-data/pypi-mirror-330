# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""Helper classes that interact with SageMaker Training service."""
from __future__ import absolute_import
import dataclasses

import os
import shutil

from typing import Callable, List, Optional, Union
from urllib.parse import urlparse

from positron_job_runner.runtime_environment_manager import (
    _running_in_conda,
    _get_python_version_from_conda_yaml
)
from common.custom_file_filter import (
    CustomFileFilter,
    copy_workdir
)
from common.config import PositronJob
from common.logging_config import logger
from common.utils import ( 
    _tmpdir
)
from common.print_banner import workspace_file_tree
from common.console import console, ROBBIE_YELLOW

from common.aws.s3 import S3Uploader

# runtime script names
BOOTSTRAP_SCRIPT_NAME = "bootstrap_runtime_environment.py"
ENTRYPOINT_SCRIPT_NAME = "job_driver.sh"
PRE_EXECUTION_SCRIPT_NAME = "pre_exec.sh"
RUNTIME_MANAGER_SCRIPT_NAME = "runtime_environment_manager.py"
SPARK_APP_SCRIPT_NAME = "spark_app.py"

# training channel names
RUNTIME_SCRIPTS_CHANNEL_NAME = "sagemaker_remote_function_bootstrap"
REMOTE_FUNCTION_WORKSPACE = "sm_rf_user_ws"
JOB_REMOTE_FUNCTION_WORKSPACE = "workspace"
SCRIPT_AND_DEPENDENCIES_CHANNEL_NAME = "pre_exec_script_and_deps"

JOBS_CONTAINER_ENTRYPOINT = [
    "/bin/bash",
    f"/opt/ml/input/data/{RUNTIME_SCRIPTS_CHANNEL_NAME}/{ENTRYPOINT_SCRIPT_NAME}",
]

ENTRYPOINT_SCRIPT = f"""
#!/bin/bash

# Entry point for bootstrapping runtime environment and invoking remote function

set -eu

PERSISTENT_CACHE_DIR=${{SAGEMAKER_MANAGED_WARMPOOL_CACHE_DIRECTORY:-/opt/ml/cache}}
export CONDA_PKGS_DIRS=${{PERSISTENT_CACHE_DIR}}/sm_remotefunction_user_deps_cache/conda/pkgs
printf "INFO: CONDA_PKGS_DIRS is set to '$CONDA_PKGS_DIRS'\\n"
export PIP_CACHE_DIR=${{PERSISTENT_CACHE_DIR}}/sm_remotefunction_user_deps_cache/pip
printf "INFO: PIP_CACHE_DIR is set to '$PIP_CACHE_DIR'\\n"


printf "INFO: Bootstraping runtime environment.\\n"
python /opt/ml/input/data/{RUNTIME_SCRIPTS_CHANNEL_NAME}/{BOOTSTRAP_SCRIPT_NAME} "$@"

if [ -d {JOB_REMOTE_FUNCTION_WORKSPACE} ]
then
    if [ -f "remote_function_conda_env.txt" ]
    then
        cp remote_function_conda_env.txt {JOB_REMOTE_FUNCTION_WORKSPACE}/remote_function_conda_env.txt
    fi
    printf "INFO: Changing workspace to {JOB_REMOTE_FUNCTION_WORKSPACE}.\\n"
    cd {JOB_REMOTE_FUNCTION_WORKSPACE}
fi

if [ -f "remote_function_conda_env.txt" ]
then
    conda_env=$(cat remote_function_conda_env.txt)

    if which mamba >/dev/null; then
        conda_exe="mamba"
    else
        conda_exe="conda"
    fi

    printf "INFO: Invoking remote function inside conda environment: $conda_env.\\n"
    $conda_exe run -n $conda_env python -m sagemaker.remote_function.invoke_function "$@"
else
    printf "INFO: No conda env provided. Invoking remote function\\n"
    python -m sagemaker.remote_function.invoke_function "$@"
fi
"""

ENTRYPOINT_TORCHRUN_SCRIPT = f"""
#!/bin/bash

# Entry point for bootstrapping runtime environment and invoking remote function with torchrun

set -eu

PERSISTENT_CACHE_DIR=${{SAGEMAKER_MANAGED_WARMPOOL_CACHE_DIRECTORY:-/opt/ml/cache}}
export CONDA_PKGS_DIRS=${{PERSISTENT_CACHE_DIR}}/sm_remotefunction_user_deps_cache/conda/pkgs
printf "INFO: CONDA_PKGS_DIRS is set to '$CONDA_PKGS_DIRS'\\n"
export PIP_CACHE_DIR=${{PERSISTENT_CACHE_DIR}}/sm_remotefunction_user_deps_cache/pip
printf "INFO: PIP_CACHE_DIR is set to '$PIP_CACHE_DIR'\\n"


printf "INFO: Bootstraping runtime environment.\\n"
python /opt/ml/input/data/{RUNTIME_SCRIPTS_CHANNEL_NAME}/{BOOTSTRAP_SCRIPT_NAME} "$@"

if [ -d {JOB_REMOTE_FUNCTION_WORKSPACE} ]
then
    if [ -f "remote_function_conda_env.txt" ]
    then
        cp remote_function_conda_env.txt {JOB_REMOTE_FUNCTION_WORKSPACE}/remote_function_conda_env.txt
    fi
    printf "INFO: Changing workspace to {JOB_REMOTE_FUNCTION_WORKSPACE}.\\n"
    cd {JOB_REMOTE_FUNCTION_WORKSPACE}
fi

if [ -f "remote_function_conda_env.txt" ]
then
    conda_env=$(cat remote_function_conda_env.txt)

    if which mamba >/dev/null; then
        conda_exe="mamba"
    else
        conda_exe="conda"
    fi

    printf "INFO: Invoking remote function with torchrun inside conda environment: $conda_env.\\n"
    $conda_exe run -n $conda_env torchrun --nproc_per_node $NPROC_PER_NODE \
    -m sagemaker.remote_function.invoke_function "$@"
else
    printf "INFO: No conda env provided. Invoking remote function with torchrun\\n"
    torchrun --nproc_per_node $NPROC_PER_NODE -m sagemaker.remote_function.invoke_function "$@"
fi
"""

def _prepare_and_upload_runtime_scripts(
    use_torchrun: bool = False,
    nproc_per_node: int = 1,
):
    """Copy runtime scripts to a folder and upload to S3.

    In case of remote function, s3_base_uri is s3_root_uri + function_name.
    In case of pipeline, s3_base_uri is s3_root_uri + pipeline_name. The runtime scripts are
    uploaded only once per pipeline.

    Args:
        spark_config (SparkConfig): remote Spark job configurations.

        s3_base_uri (str): S3 location that the runtime scripts will be uploaded to.

        s3_kms_key (str): kms key used to encrypt the files uploaded to S3.

        sagemaker_session (str): SageMaker boto client session.

        use_torchrun (bool): Whether to use torchrun or not.

        nproc_per_node (int): Number of processes per node.
    """

    with _tmpdir() as bootstrap_scripts:

        # write entrypoint script to tmpdir
        entrypoint_script_path = os.path.join(bootstrap_scripts, ENTRYPOINT_SCRIPT_NAME)
        entry_point_script = ENTRYPOINT_SCRIPT

        if use_torchrun:
            entry_point_script = ENTRYPOINT_TORCHRUN_SCRIPT
            entry_point_script = entry_point_script.replace("$NPROC_PER_NODE", str(nproc_per_node))

        with open(entrypoint_script_path, "w", newline="\n") as file:
            file.writelines(entry_point_script)

        bootstrap_script_path = os.path.join(
            os.path.dirname(__file__), "runtime_environment", BOOTSTRAP_SCRIPT_NAME
        )
        runtime_manager_script_path = os.path.join(
            os.path.dirname(__file__), "runtime_environment", RUNTIME_MANAGER_SCRIPT_NAME
        )

        # copy runtime scripts to tmpdir
        shutil.copy2(bootstrap_script_path, bootstrap_scripts)
        shutil.copy2(runtime_manager_script_path, bootstrap_scripts)

        """"
        upload_path = S3Uploader.upload(
            bootstrap_scripts,
            s3_path_join(s3_base_uri, RUNTIME_SCRIPTS_CHANNEL_NAME),
            s3_kms_key,
            sagemaker_session,
        )
        return upload_path
        """
        return None
        

def _prepare_deps_and_pre_execution_scripts(
    local_deps_path: str,
    pre_execution_commands: List[str],
    pre_execution_script_local_path: str,
    tmp_dir: str,
):
    """Prepare pre-execution scripts and deps and upload them to s3.

    If pre execution commands are provided, a new bash file will be created
      with those commands in tmp directory.
    If pre execution script is provided, it copies that file from local file path
      to tmp directory.
    If local deps file is provided, it copies that file from local file path
      to tmp directory.
    If under pipeline context, tmp directory with copied deps and scripts is
      uploaded to S3.
    """

    if not (local_deps_path or pre_execution_commands or pre_execution_script_local_path):
        return None

    if local_deps_path:
        dst_path = shutil.copy2(local_deps_path, tmp_dir)
        # workspace_file_tree.add(f"[yellow]{os.path.basename(local_deps_path)}, size: {os.path.getsize(local_deps_path)} bytes[/yellow]")
        logger.info("Copied deps file at '%s' to '%s'", local_deps_path, dst_path)

    if pre_execution_commands or pre_execution_script_local_path:
        pre_execution_script = os.path.join(tmp_dir, PRE_EXECUTION_SCRIPT_NAME)
        if pre_execution_commands:
            with open(pre_execution_script, "w") as target_script:
                commands = [cmd + "\n" for cmd in pre_execution_commands]
                target_script.writelines(commands)
                logger.info(
                    "Generated pre-execution script from commands to '%s'", pre_execution_script
                )
        else:
            shutil.copy2(pre_execution_script_local_path, pre_execution_script)
            logger.info(
                "Copied pre-execution commands from script at '%s' to '%s'",
                pre_execution_script_local_path,
                pre_execution_script,
            )
    return None

def _prepare_and_upload_workspace(
    job_id: str,
    local_deps_path: str,
    include_local_workdir: bool,
    pre_execution_commands: List[str],
    pre_execution_script_local_path: str,
    custom_file_filter: Optional[Union[Callable[[str, List], List], CustomFileFilter]] = None,
) -> str:
    """Prepare and upload the workspace to S3. """

    if not (
        local_deps_path
        or include_local_workdir
        or pre_execution_commands
        or pre_execution_script_local_path
    ):
        return None

    with _tmpdir() as tmp_dir:
        tmp_workspace_dir = os.path.join(tmp_dir, "temp_workspace/")
        os.mkdir(tmp_workspace_dir)
        
        # TODO Remove the following hack to avoid dir_exists error in the copy_tree call below.
        # UPDATE: fixed with the dirs_exist_ok=True flag in the copy_tree call below.
        # tmp_workspace = os.path.join(tmp_workspace_dir, JOB_REMOTE_FUNCTION_WORKSPACE)

        tmp_workspace = tmp_workspace_dir

        if include_local_workdir:
            copy_workdir(
                dst=tmp_workspace, 
                custom_file_filter=custom_file_filter,
                print_tree=False)
            logger.info(f"Copied local directory {os.getcwd()} to '%s'", tmp_workspace)

        if not os.path.isdir(tmp_workspace):
            # create the directory if no workdir_path was provided in the input.
            os.mkdir(tmp_workspace)

        _prepare_deps_and_pre_execution_scripts(
            local_deps_path=local_deps_path,
            pre_execution_commands=pre_execution_commands,
            pre_execution_script_local_path=pre_execution_script_local_path,
            tmp_dir=tmp_workspace,
        )

        workspace_archive_path = os.path.join(tmp_dir, "workspace")
        workspace_archive_path = shutil.make_archive(
            workspace_archive_path, 
            "zip", 
            tmp_workspace_dir
        )
        logger.info("Successfully created workdir archive at '%s'", workspace_archive_path)

        upload_path = S3Uploader.upload_file(
            workspace_archive_path,
            job_id,
            "workspace.zip"
        )

        logger.info("Successfully uploaded workdir to '%s'", upload_path)
        return upload_path


