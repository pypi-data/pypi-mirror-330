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
"""An entry point for runtime environment. This must be kept independent of SageMaker PySDK"""
from __future__ import absolute_import

import argparse
import getpass
import sys
import os
import shutil
import pathlib

if (os.getenv('POSITRON_CLOUD_ENVIRONMENT')):
    from positron_job_runner.cloud_logger import logger
else:
    from common.logging_config import logger

from positron_job_runner.runtime_environment_manager import (
        RuntimeEnvironmentManager,
        _DependencySettings,
        _run_shell_cmd
)
from positron_job_runner.runner_env import runner_env

SUCCESS_EXIT_CODE = 0
DEFAULT_FAILURE_CODE = 1

REMOTE_FUNCTION_WORKSPACE = "sm_rf_user_ws"
BASE_CHANNEL_PATH = "/opt/ml/input/data"
FAILURE_REASON_PATH = "/opt/ml/output/failure"
JOB_OUTPUT_DIRS = ["/opt/ml/output", "/opt/ml/model", "/tmp"]
PRE_EXECUTION_SCRIPT_NAME = "pre_exec.sh"
JOB_REMOTE_FUNCTION_WORKSPACE = "workspace"
SCRIPT_AND_DEPENDENCIES_CHANNEL_NAME = "pre_exec_script_and_dependencies"


def _bootstrap_runtime_env(
    client_python_version: str,
    conda_env: str = None,
    dependency_settings: _DependencySettings = None,
    pre_exec_commands: str = None,
):
    """Bootstrap runtime environment for remote function invocation.

    Args:
        client_python_version (str): Python version at the client side.
        conda_env (str): conda environment to be activated. Default is None.
        dependency_settings (dict): Settings for installing dependencies.
    """

    workspace_unpack_dir = _unpack_user_workspace()
    if not workspace_unpack_dir:
        logger.info("No workspace to unpack and setup.")
        return

    print("workspace_unpack_dir: ", workspace_unpack_dir)
    
    # FUTURE Use
    #_handle_pre_exec_commands(pre_exec_commands)

    _install_dependencies(
        dependency_file_dir = workspace_unpack_dir,
        conda_env = conda_env,
        client_python_version = client_python_version,
        dependency_settings = dependency_settings,
    )

def _handle_pre_exec_commands(commands: str):
    """Run the pre execution commands."""
    if commands == None or commands == "":
        logger.info("No pre-execution commands to run.")
    else:
        logger.info("Running pre-execution commands.")
        _run_shell_cmd(commands)
        logger.info("Finished running pre-execution commands.")


def _install_dependencies(
    dependency_file_dir: str,
    conda_env: str,
    client_python_version: str,
    dependency_settings: _DependencySettings = None,
):
    """Install dependencies in the job container

    Args:
        dependency_file_dir (str): Directory in the container where dependency file exists.
        conda_env (str): conda environment to be activated.
        client_python_version (str): Python version at the client side.
        dependency_settings (dict): Settings for installing dependencies.
    """

    if dependency_settings is not None and dependency_settings.dependency_file is None:
        # an empty dict is passed when no dependencies are specified
        logger.info("No dependencies to install.")
    elif dependency_settings is not None:
        dependencies_file = os.path.join(dependency_file_dir, dependency_settings.dependency_file)
        RuntimeEnvironmentManager().bootstrap(
            local_dependencies_file=dependencies_file,
            conda_env=conda_env,
            client_python_version=client_python_version,
        )
    '''
    else:
        # no dependency file name is passed when an older version of the SDK is used
        # we look for a file with .txt, .yml or .yaml extension in the workspace directory
        dependencies_file = None
        for file in os.listdir(dependency_file_dir):
            if file.endswith(".txt") or file.endswith(".yml") or file.endswith(".yaml"):
                dependencies_file = os.path.join(dependency_file_dir, file)
                break

        if dependencies_file:
            RuntimeEnvironmentManager().bootstrap(
                local_dependencies_file=dependencies_file,
                conda_env=conda_env,
                client_python_version=client_python_version,
            )
        else:
            logger.info(
                "Did not find any dependency file in the directory at '%s'."
                " Assuming no additional dependencies to install.",
                os.path.join(BASE_CHANNEL_PATH, channel_name),
            )
    '''


def _unpack_user_workspace():
    """Unzip the user workspace"""

    """
    workspace_archive_dir_path = os.path.join(BASE_CHANNEL_PATH, REMOTE_FUNCTION_WORKSPACE)

    if not os.path.exists(workspace_archive_dir_path):
        logger.info(
            "Directory '%s' does not exist.",
            workspace_archive_dir_path,
        )
        return None
    """

    workspace_archive_dir_path = runner_env.JOB_CWD

    workspace_archive_path = os.path.join(workspace_archive_dir_path, "workspace.zip")
    if not os.path.isfile(workspace_archive_path):
        logger.info(
            f"Workspace archive '{workspace_archive_dir_path}' does not exist.",
        )
        return None

    # workspace_unpack_dir = pathlib.Path(os.getcwd()).absolute()
    workspace_unpack_dir = runner_env.JOB_CWD
    

    print(f"_unpack_user_workspace(): workspace_archive_path: {workspace_archive_path}, workspace_unpack_dir: {workspace_unpack_dir}")
    '''
    shutil.unpack_archive(
        filename=workspace_archive_path, 
        extract_dir=workspace_unpack_dir,
        format = "zip"
    )
    '''
    _run_shell_cmd(f'unzip {workspace_archive_path} -d {workspace_unpack_dir}')
    logger.info(f"Successfully unpacked workspace archive at '{workspace_unpack_dir}'.")

    # workspace_unpack_dir = pathlib.Path(workspace_unpack_dir, JOB_REMOTE_FUNCTION_WORKSPACE)
    return workspace_unpack_dir


def _write_failure_reason_file(failure_msg):
    """Create a file 'failure' with failure reason written if bootstrap runtime env failed.

    See: https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-training-algo.html
    Args:
        failure_msg: The content of file to be written.
    """
    if not os.path.exists(FAILURE_REASON_PATH):
        with open(FAILURE_REASON_PATH, "w") as f:
            f.write("RuntimeEnvironmentError: " + failure_msg)

