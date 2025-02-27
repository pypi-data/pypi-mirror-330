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
"""robbie runtime environment module. This must be kept independent of robbie PySDK"""

from __future__ import absolute_import


# import logging
import sys
import shlex
import os
import subprocess
import threading
import select
import time
import yaml
import dataclasses
import json
import importlib.metadata
import platform
import argparse
import re
import json

# command runner modes
CONDA_MODE = "conda"
PYTHON_MODE = "python"
GENERIC_MODE = "generic"

if (os.getenv('POSITRON_CLOUD_ENVIRONMENT')):
    from positron_job_runner.cloud_logger import logger
    logger.debug("RuntimeEnvironmentManager: Running in cloud environment")
else:
    from common.logging_config import logger
    logger.debug("RuntimeEnvironmentManager: NOT running in cloud environment")


@dataclasses.dataclass
class _DependencySettings:
    """Dependency settings for the remote function.

    Instructs the runtime environment script on how to handle dependencies.
    If ``dependency_file`` is set, the runtime environment script will attempt
    to install the dependencies. If ``dependency_file`` is not set, the runtime
    environment script will assume no dependencies are required.
    """

    dependency_file: str = None

    def to_string(self):
        """Converts the dependency settings to a string."""
        return json.dumps(dataclasses.asdict(self))

    @staticmethod
    def from_string(dependency_settings_string):
        """Converts a json string to dependency settings.

        Args:
            dependency_settings_string (str): The json string to convert.
        """
        if dependency_settings_string is None:
            return None
        dependency_settings_dict = json.loads(dependency_settings_string)
        return _DependencySettings(dependency_settings_dict.get("dependency_file"))

    @staticmethod
    def from_dependency_file_path(dependency_file_path):
        """Converts a dependency file path to dependency settings.

        Args:
            dependency_file_path (str): The path to the dependency file.
        """
        if dependency_file_path is None:
            return _DependencySettings()
        if dependency_file_path == "auto-capture":
            return _DependencySettings("env_snapshot.yml")
        return _DependencySettings(os.path.basename(dependency_file_path))


class RuntimeEnvironmentManager:
    """Runtime Environment Manager class to manage runtime environment."""

    def snapshot(self, dependencies: str) -> str:
        """Creates snapshot of the user's environment

        If a req.txt or conda.yml file is provided, it verifies their existence and
        returns the local file path
        If ``auto_capture`` is set, this method will take the snapshot of
        user's dependencies installed in the local runtime.
        Current support for ``auto_capture``:
        * conda env, generate a yml file and return it's local path
        * pip env, generate a requirements.txt file and return it's local path

        Args:
            dependencies (str): dependencies file path or "auto-capture"

        Returns:
            file path of the existing or generated dependencies file
        """

        # No additional dependencies specified
        if dependencies is None:
            return None
        
        if dependencies == "auto-capture":
            if os.getenv("CONDA_DEFAULT_ENV"):
                # we are running in a conda environment
                return self._capture_from_conda_runtime()
            else:
                # we are not running on a conda environment
                return self._capture_from_pip_runtime()
        elif dependencies == "auto-capture-pip":
            return self._capture_deps_from_py_files()

        if dependencies == "none":
            return "none"
        # Dependencies specified as either req.txt or conda_env.yml
        if (
            dependencies.endswith(".txt")
            or dependencies.endswith(".yml")
            or dependencies.endswith(".yaml")
        ):
            self._is_file_exists(dependencies)
            return dependencies

        raise ValueError(f'Invalid dependencies provided: "{dependencies}"')

    def _pipdeptree_list(self, remove_robbie: bool = False) -> dict:
        
        def extract_packages(dependencies, package_dict):
            for dep in dependencies:
                package_dict[dep["package_name"]] = dep["installed_version"]
                extract_packages(dep["dependencies"], package_dict)

        # Get the dependency tree from pipdeptree
        result = subprocess.run(
                    "pipdeptree --json-tree",
                    capture_output=True,
                    text=True,
                    check=True,
                    shell=True,
                )
        dependency_tree = json.loads(result.stdout)

        # Extract remaining packages
        remaining_packages = {}
        extract_packages(dependency_tree, remaining_packages)

        # Define packages to remove (top-level only)
        if remove_robbie:
            if "robbie" in remaining_packages:
                del remaining_packages["robbie"]

        # For Windows local machines, remove pywin32 package
        if "pywin32" in remaining_packages:
            del remaining_packages["pywin32"]
        
        if "windows-curses" in remaining_packages:
            del remaining_packages["windows-curses"]
        
        return remaining_packages


    def _capture_from_pip_runtime(self, output_file = "requirements.txt") -> str:

        remaining_packages = self._pipdeptree_list(remove_robbie=True)

        # Write dependencies to requirements.txt
        with open(output_file, "w", encoding="utf-8") as file:
            for pkg, version in sorted(remaining_packages.items()):
                file.write(f"{pkg}=={version}\n")
       
        logger.debug(f"_capture_from_pip_runtime: returning")
        return os.path.join(os.getcwd(), output_file)

    def _capture_from_conda_runtime(self) -> str:
        """Generates dependencies list from the user's local runtime.

        Raises RuntimeEnvironmentError if not able to.

        Currently supports: conda environments
        """

        # Try to capture dependencies from the conda environment, if any.
        conda_env_name = self._get_active_conda_env_name()
        conda_env_prefix = self._get_active_conda_env_prefix()
        if conda_env_name:
            logger.info(f"Found conda_env_name: '{conda_env_name}'")
        elif conda_env_prefix:
            logger.info(f"Found conda_env_prefix: '{conda_env_prefix}'")
        else:
            raise ValueError("No conda environment seems to be active.")

        if conda_env_name == "base":
            logger.warning(
                "We recommend using an environment other than base to "
                "isolate your project dependencies from conda dependencies"
            )

        local_dependencies_path = os.path.join(os.getcwd(), "env_snapshot.yml")
        self._export_conda_env_from_prefix(conda_env_prefix, local_dependencies_path)

        return local_dependencies_path
    
    def _capture_deps_from_py_files(self) -> str:
        """
        Generates a requirement.txt from the .py files in the current directory
        See pipreqs package - https://github.com/bndr/pipreqs
        """
        logger.debug("Generating requirements.txt from the .py files in the current directory")
        _run_shell_cmd(f"pipreqs --force .")
        # this is a hack to remove the robbie package from the requirements.txt file
        _remove_package_from_requirements('robbie') 
        logger.debug(f"_capture_deps_from_py_files: returning")
        return os.path.join(os.getcwd(), "requirements.txt")

    def _get_active_conda_env_prefix(self) -> str:
        """Returns the conda prefix from the set environment variable. None otherwise."""
        return os.getenv("CONDA_PREFIX")

    def _get_active_conda_env_name(self) -> str:
        """Returns the conda environment name from the set environment variable. None otherwise."""
        return os.getenv("CONDA_DEFAULT_ENV")

    # @logger_module(module="Installing dependencies")
    def bootstrap(
        self, local_dependencies_file: str, client_python_version: str, conda_env: str = None
    ):
        """Bootstraps the runtime environment by installing the additional dependencies if any.

        Args:
            local_dependencies_file (str): path where dependencies file exists.
            conda_env (str): conda environment to be activated. Default is None.

        Returns: None
        """

        if local_dependencies_file.endswith(".txt"):
            if conda_env:
                self._install_req_txt_in_conda_env(conda_env, local_dependencies_file)
                #self._write_conda_env_to_file(conda_env)

            else:
                self._install_requirements_txt(local_dependencies_file, _python_executable())

        elif local_dependencies_file.endswith(".yml") or local_dependencies_file.endswith(".yaml"):
            """
            if conda_env:
                self._update_conda_env(conda_env, local_dependencies_file)
            else:
                conda_env = "robbie-runtime-env"
            """ 
            self._create_conda_env(conda_env, local_dependencies_file)
            # We will do this at a higher level depending upon the use case
            # self._validate_python_version(client_python_version, conda_env)
            # self._write_conda_env_to_file(conda_env)


    def change_dir_permission(self, dirs: list, new_permission: str):
        """Change the permission of given directories

        Args:
            dirs (list[str]): A list of directories for permission update.
            new_permission (str): The new permission for the given directories.
        """

        _ERROR_MSG_PREFIX = "Failed to change directory permissions due to: "
        command = ["sudo", "chmod", "-R", new_permission] + dirs
        logger.info(f"Executing {' '.join(command)}.")

        try:
            subprocess.run(command, check=True, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as called_process_err:
            err_msg = called_process_err.stderr.decode("utf-8")
            raise RuntimeEnvironmentError(f"{_ERROR_MSG_PREFIX} {err_msg}")
        except FileNotFoundError as file_not_found_err:
            if "[Errno 2] No such file or directory: 'sudo'" in str(file_not_found_err):
                raise RuntimeEnvironmentError(
                    f"{_ERROR_MSG_PREFIX} {file_not_found_err}. "
                    "Please contact the image owner to install 'sudo' in the job container "
                    "and provide sudo privilege to the container user."
                )
            raise RuntimeEnvironmentError(file_not_found_err)

    def _is_file_exists(self, dependencies):
        """Check whether the dependencies file exists at the given location.

        Raises error if not
        """
        if not os.path.isfile(dependencies):
            raise ValueError(f'No dependencies file named: {dependencies} was found.')

    def _install_requirements_txt(self, local_path, python_executable):
        """Install requirements.txt file"""
        #TODO: Add support for pipenv if necessary
        cmd = f"{python_executable} -m pip install -r {local_path} -U"
        logger.info(f"Running command: '{cmd}' in the dir: '{os.getcwd()}'")
        _run_shell_cmd(cmd)
        logger.info(f"Command {cmd} ran successfully")

    def _install_pip_package_from_dir(self, initial_cmd, local_path):
        """Install requirements.txt file"""
        #TODO: Add support for pipenv if necessary
        cmd = f"{initial_cmd} && {_python_executable()} -m pip install {local_path} -U"
        logger.info(f"Running command: {cmd} in the dir: {os.getcwd()}")
        _run_shell_cmd(cmd)
        logger.info(f"Command {cmd} ran successfully")


    def _create_conda_env(self, env_name, local_path):
        """Create conda env using conda yml file"""

        logger.info(f"_create_conda_env(): Current UID:{os.getuid()}, Current GID:{os.getgid()}")

        cmd = f"{self._get_conda_exe()} env create -n {env_name} --file {local_path}"
        # cmd = f"/opt/conda/bin/mamba env create -n {env_name} --file {local_path}"
        
        logger.info(f"Creating conda environment {env_name} using: {cmd}")
        _run_shell_cmd(cmd)
        logger.info(f"Conda environment: {env_name} created successfully.")

    def _install_req_txt_in_conda_env(self, env_name, local_path):
        """Install requirements.txt in the given conda environment"""

        cmd = f"{self._get_conda_exe()} run -n {env_name} pip install -r {local_path} -U"
        logger.info(f"Activating conda env and installing requirements: {cmd}")
        _run_shell_cmd(cmd)
        logger.info(f"Requirements installed successfully in conda env {env_name}")

    def _install_pip_package_from_dir_in_conda_env(self, env_name, package_dir):
        """Install pip package in the given conda environment"""

        cmd = f"{self._get_conda_exe()} run -n {env_name} pip install {package_dir}  -U"
        logger.info(f"Activating conda env and installing requirements: {cmd}")
        _run_shell_cmd(cmd)
        logger.info(f"Requirements installed successfully in conda env {env_name}")

    def _update_conda_env(self, env_name, local_path):
        """Update conda env using conda yml file"""

        cmd = f"{self._get_conda_exe()} env update -n {env_name} --file {local_path}"
        logger.info(f"Updating conda env: {cmd}")
        _run_shell_cmd(cmd)
        logger.info(f"Conda env {env_name} updated succesfully")

    '''
    def _export_conda_env_from_prefix(self, prefix, local_path):
        """Export the conda env to a conda yml file"""

        logger.info(f"Exporting conda environment: {prefix} to {local_path}")

        if platform.system() == "Windows":
            logger.info(f"Exporting Windows conda environment.")
            self._windows_conda_export(prefix, local_path)
        else:
            # cmd = f"{self._get_conda_exe()} env export -p {prefix} --no-builds > {local_path}"
            # logger.info(f"Exporting {platform.system()} conda environment: {cmd}")
            #_run_shell_cmd(cmd)
            self._nix_conda_export(prefix, local_path)
            logger.info(f"Conda environment {prefix} exported successfully")
    '''

    def _export_conda_env_from_prefix(self, prefix, output_file):
        """
        Export the current conda environment, including pip packages, to a specified YAML file.
        """
        # Construct the conda command based on the prefix (if provided)
        prefix_option = f"--prefix {prefix}"

        formatted_pip_packages = []
        pip_packages = self._pipdeptree_list(remove_robbie=False)
        for pkg, version in sorted(pip_packages.items()):
            formatted_pip_packages.append(f"      - {pkg.lower()}=={version}")

        # Export conda environment with history (without builds)
        history_env_proc = subprocess.run(
            "conda env export --from-history " + prefix_option,
            capture_output=True, text=True, check=True, shell=True
        )
        history_env = history_env_proc.stdout

        # Remove "prefix" line from history export
        history_env_lines = [line for line in history_env.splitlines() if not line.startswith("prefix:")]

        # Ensure the "- pip" line is present
        if not any(line.strip() == "- pip" for line in history_env_lines):
            history_env_lines.append("  - pip")
        history_env_lines.append("  - pip:")

        # Combine environment with pip packages
        environment_yml = "\n".join(history_env_lines) + "\n" + "\n".join(formatted_pip_packages)

        # Write to the specified file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(environment_yml)

        logger.info(f"Exported environment to: {output_file}")


    # TODO: remove this since its not used.
    def _windows_conda_export(self, prefix, output_file):
        """
        Export the current conda environment, including pip packages, to a specified YAML file.

        Args:
            prefix (str): The path to the conda environment. If None, uses the current active environment.
            output_file (str): The name of the output YAML file. Defaults to "environment.yml".
        """
        # Construct the conda command based on the prefix (if provided)
        prefix_option = f"--prefix {prefix}"

        # Export the full conda environment
        full_env_proc = subprocess.run(
            "conda env export " + prefix_option,
            capture_output=True, text=True, check=True, shell=True
        )
        full_env = full_env_proc.stdout

        # Extract pip packages
        pip_packages = []
        in_pip_section = False
        for line in full_env.splitlines():
            if "- pip:" in line:
                in_pip_section = True
                pip_packages.append(line)  # Keep the "- pip:" line
            elif in_pip_section:
                if line.startswith("      - "):  # Indented package names
                    if "pywin32" in line:  # Skip pywin32 package on Windows
                        continue
                    else:
                        pip_packages.append(line)
                else:
                    break  # End of pip section
        # Export conda environment with history (without builds)
        history_env_proc = subprocess.run(
            "conda env export --from-history " + prefix_option,
            capture_output=True, text=True, check=True, shell=True
        )
        history_env = history_env_proc.stdout

        # Remove "prefix" line from history export
        history_env_lines = [line for line in history_env.splitlines() if not line.startswith("prefix:")]

        # Ensure the "- pip" line is present
        if not any(line.strip() == "- pip" for line in history_env_lines):
            history_env_lines.append("  - pip")

        # Combine environment with pip packages
        environment_yml = "\n".join(history_env_lines) + "\n" + "\n".join(pip_packages)

        # Write to the specified file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(environment_yml)

        logger.info(f"Exported environment to: {output_file}")


    def _write_conda_env_to_file(self, env_name):
        """Writes conda env to the text file"""

        file_name = "robbie_conda_env.txt"
        file_path = os.path.join(os.getcwd(), file_name)
        with open(file_path, "w") as output_file:
            output_file.write(env_name)

    def _get_conda_exe(self):
        """Checks whether conda or mamba is available to use"""
        
        if (os.getenv('POSITRON_CLOUD_ENVIRONMENT')):
            logger.debug('_get_conda_exe(): running in cloud environment')
            return "/opt/conda/bin/mamba"
        else:
            # client 
            logger.debug("_get_conda_exe(): running in local or non 'job_user' cloud environment")
            import platform

            if platform.system() == "Windows":
                logger.debug("Running on Windows")
                which = "where"
            else:
                logger.debug("Not running on Windows")
                which = "which"

            if not subprocess.Popen([which, "mamba"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait():
                return "mamba"
            if not subprocess.Popen([which, "conda"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait():
                return "conda"
            raise ValueError("Neither conda nor mamba is installed or in the PATH")
            '''
            logger.debug'_get_conda_exe(): running in cloud environment')
            from .runner_env import runner_env 

            logger.debug"local environment: ", os.environ)
            logger.debug("runner_env: ", runner_env.env_without_runner_env())

            if (runner_env.JOB_USER == 'job_user'):
                logger.debug(f"_get_conda_exe(): Running as protected user")

                if not subprocess.Popen(
                    # ["which", "mamba"],
                    ["su", "-c", "test -f /opt/conda/bin/mamba", "-s", "/bin/bash", runner_env.JOB_USER],
                    env=runner_env.env_without_runner_env()
                ).wait():
                    return "mamba"
                raise ValueError("Neither conda nor mamba is installed on the image")


                result = subprocess.Popen(
                    ["su", "-c", "env", "-s", "/bin/bash", runner_env.JOB_USER], 
                    # capture_output=True, 
                    text=True,
                    env=runner_env.env_without_runner_env(),
                )
                if result.returncode == 0:
                    logger.debug(result.stdout)
                else:
                    logger.debug(f"print env ({result.returncode}): {result.stderr}")

                result = subprocess.Popen(
                    ["su", "-c", "which mamba", "-s", "/bin/bash", runner_env.JOB_USER], 
                    # capture_output=True, 
                    text=True,
                    env=runner_env.env_without_runner_env(),
                )
                if result.returncode == 0:
                    return result.stdout.strip()
                else:
                    logger.debug(f"Checking for mamba error ({result.returncode}): {result.stderr}")
        
                result = subprocess.Popen(
                    ["su", "-c", "which conda", "-s", "/bin/bash", runner_env.JOB_USER], 
                    # capture_output=True, 
                    text=True,
                    env=runner_env.env_without_runner_env(),
                )
                if result.returncode == 0:
                    return result.stdout.strip()
                else:
                    logger.debug(f"Checking for conda error ({result.returncode}): {result.stderr}")

                raise ValueError("Neither conda nor mamba is installed on the image")
                '''

    def _python_version_in_conda_env(self, env_name):
        """Returns python version inside a conda environment"""
        if not env_name:
            return None
        
        base_cmd = f"{self._get_conda_exe()} run -n {env_name} python --version"

        if (os.getenv('POSITRON_CLOUD_ENVIRONMENT')):
            logger.debug('_python_version_in_conda_env(): running in cloud environment')
            from .runner_env import runner_env 

            if (runner_env.JOB_USER == 'job_user'):
                logger.debug(f"_python_version_in_conda_env(): Running as protected user")
                cmd = f"su -c '{base_cmd}' -s /bin/bash job_user"
                try:
                    output = (
                        subprocess.check_output(shlex.split(cmd), 
                                                stderr=subprocess.STDOUT, 
                                                env=runner_env.env_without_runner_env(),
                                                cwd=runner_env.JOB_CWD)
                        .decode("utf-8")
                        .strip()
                    )
                    # convert 'Python 3.7.16' to [3, 7, 16]
                    version = output.split("Python ")[1].split(".")
                    return version[0] + "." + version[1]
                except subprocess.CalledProcessError as e:
                    raise RuntimeEnvironmentError(e.output)
                
        logger.debug(f"_python_version_in_conda_env(): Running as local or non-protected user")      
        try:
            output = (
                subprocess.check_output(base_cmd, stderr=subprocess.STDOUT, shell=True)
                .decode("utf-8")
                .strip()
            )
            # convert 'Python 3.7.16' to [3, 7, 16]
            version = output.split("Python ")[1].split(".")
            return version[0] + "." + version[1]
        except subprocess.CalledProcessError as e:
            raise RuntimeEnvironmentError(e.output)

    def _current_python_version(self):
        """Returns the current python version where program is running"""

        return f"{sys.version_info.major}.{sys.version_info.minor}".strip()

    def _current_robbie_pysdk_version(self):
        """Returns the current robbie python sdk version where program is running"""
        '''
        try:
            import robbie
            version = robbie.__version__
        except Exception as e:
            return f"Failed to retrieve robbie version due to: {e}"
        return version
        '''
        return importlib.metadata.version('robbie')

    def _validate_python_version(self, client_python_version: str, conda_env: str = None):
        """Validate the python version

        Validates if the python version where remote function runs
        matches the one used on client side.
        """
        if conda_env:
            job_python_version = self._python_version_in_conda_env(conda_env)
        else:
            job_python_version = self._current_python_version()
            
        if not job_python_version or client_python_version.strip() != job_python_version.strip():
            raise RuntimeEnvironmentError(
                f"Python version found in the container is '{job_python_version}' which "
                f"does not match python version '{client_python_version}' on the local client. "
                f"Please make sure that the python version used in the training container "
                f"is same as the local python version."
            )

    def _validate_robbie_pysdk_version(self, client_robbie_pysdk_version):
        """Validate the robbie python sdk version

        Validates if the robbie python sdk version where remote function runs
        matches the one used on client side.
        Otherwise, log a warning to call out that unexpected behaviors
        may occur in this case.
        """
        job_robbie_pysdk_version = self._current_robbie_pysdk_version()
        if (
            client_robbie_pysdk_version
            and client_robbie_pysdk_version != job_robbie_pysdk_version
        ):
            warning_str = f"""Inconsistent robbie versions found: 
                              robbie python sdk version found in the container is 
                              {job_robbie_pysdk_version}' which does not match the '{client_robbie_pysdk_version}' on the local client. 
                              Please make sure that the robbie version used in the training container 
                              is the same as the local robbie version in case of unexpected behaviors.
            """
            logger.warning(warning_str)                     
    
    def _list_conda_environments(self):
        cmd_list = [f'{self._get_conda_exe()}', 'env', 'list']
        try:
            # Run the 'conda env list' command and capture the output
            result = subprocess.run(cmd_list, stdout=subprocess.PIPE, text=True)
        
            # Extract lines from the output, skip header and empty lines
            lines = result.stdout.splitlines()
            envs = []
        
            # Parse the environments from the output
            for line in lines[2:]:  # Skip the header rows
                if line.strip():
                    env_name = line.split()[0]  # The environment name is the first element
                    envs.append(env_name)
        
            return envs
    
        except Exception as e:
            logger.debug(f"Error listing conda environments: {e}")
            return []
        
    def _valid_conda_env(self, conda_env: str) -> bool:
        if not conda_env:
            return False
        return conda_env in RuntimeEnvironmentManager()._list_conda_environments()

def _run_and_get_output_shell_cmd(cmd: str) -> str:
    """Run and return the output of the given shell command"""
    return subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT).decode("utf-8")


def _run_shell_cmd(cmd: str):
    """
    This method runs a given shell command using subprocess
    We handle the following cases:
    - Running in a local environment
    - Running in a cloud environment
        - As the positron user
        - As the protected user
    
    """
    # logger.debug(f"_run_shell_cmd(): {cmd}")
    # cwd is driven by the client or server side execution
    if os.getenv('POSITRON_CLOUD_ENVIRONMENT'):

        # logger.debug('_run_shell_cmd(): running in cloud environment')
        from .runner_env import runner_env 

        if (runner_env.JOB_USER != 'job_user'):
            # logger.debug('_run_shell_cmd(): as current user')
            p = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True,                # allows running on any os
                # universal_newlines=True,   # otherwise stdout and stderr will be bytes
                cwd=runner_env.JOB_CWD,
            )
        else:
            # logger.debug('_run_shell_cmd(): as protected user')

            env=runner_env.env_without_runner_env()

            # Unfortunately, the PATH variable is not  passed correctly to the subprocess in `env` with the su -c command
            # The workaround is to prefix the command with the PATH variable
            new_cmd = f"PATH={env['PATH']};{cmd}"
            # logger.debug(f"new_cmd: {new_cmd}")

            p = subprocess.Popen(
                ["su", "-c", new_cmd, "-s", "/bin/bash", "job_user"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                # requires elevated permissions which is not allowed in the runtime environment.
                # shell=True,
                cwd=runner_env.JOB_CWD,
                # universal_newlines=True,
                env=env,
            )
        log_stop_event = threading.Event()
        stdout_thread = threading.Thread(target=logging_thread, args=(p.stdout, "stdout", log_stop_event)); stdout_thread.start()
        stderr_thread = threading.Thread(target=logging_thread, args=(p.stderr, "stderr", log_stop_event)); stderr_thread.start()
        return_code = p.wait()
        log_stop_event.set()
        stdout_thread.join()
        stderr_thread.join()
        if return_code:
            error_message = f"Encountered error while running command '{cmd}'"
            raise RuntimeEnvironmentError(error_message)

    else:
        # logger.debug('_run_shell_cmd(): running in local environment')
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,                # allows running on any os
            # universal_newlines=True,   # otherwise stdout and stderr will be bytes
        )
        if platform.system() == 'Windows':
        # windows insanity
            try:
                # Read both stdout and stderr line by line
                for line in p.stdout:
                    print(line, end="")  # Avoid adding extra newlines
                for line in p.stderr:
                    print("ERROR: " + line, end="")
            except UnicodeEncodeError as e:
                print(f"Unicode error encountered: {e}")
            finally:
                p.stdout.close()
                p.stderr.close()
                return_code = p.wait()
            if return_code:
                error_message = f"Encountered error while running command '{cmd}'"
                raise RuntimeEnvironmentError(error_message)
        else:
            log_stop_event = threading.Event()
            stdout_thread = threading.Thread(target=logging_thread, args=(p.stdout, "stdout", log_stop_event)); stdout_thread.start()
            stderr_thread = threading.Thread(target=logging_thread, args=(p.stderr, "stderr", log_stop_event)); stderr_thread.start()
            return_code = p.wait()
            log_stop_event.set()
            stdout_thread.join()
            stderr_thread.join()
            if return_code:
                error_message = f"Encountered error while running command '{cmd}'"
                raise RuntimeEnvironmentError(error_message)

def logging_thread(pipe, stream_name: str, stop_event: threading.Event):
    try:
        with pipe:
            while not stop_event.is_set():
                # Calling pipe.readline() will hang the process until a new line is available
                # however, if no new lines are available, we want to check if the thread should stop
                ready, _, _ = select.select([pipe], [], [], 0.1)
                if ready:
                    # TODO: Can I iterate over the pipe and process everything that's ready?
                    line = pipe.readline()
                    if not line:
                        break
                    if line.strip():
                        if stream_name == "stdout":
                            logger.debug(line.rstrip())
                        else:
                            logger.debug("ERROR: " + line.rstrip())
                else:
                    stop_event.wait(1)

            # Read one last time.
            ready, _, _ = select.select([pipe], [], [], 0.1)
            if ready:
                for line in pipe:
                    if line.strip():
                        if stream_name == "stdout":
                            logger.debug(line.rstrip())
                        else:
                            logger.debug("ERROR: " + line.rstrip())
            # TODO: Do we need to check one more time for outstanding data in the pipe?
            # logger.debug(f'Logging thread for: {stream_name} stopped')
    except RuntimeEnvironmentError as e:
        logger.debug(f'Logging thread for: {stream_name} stopped with exception: {e}')

def _python_executable():
    """Return the real path for the Python executable, if it exists.

    Return RuntimeEnvironmentError otherwise.

    Returns:
        (str): The real path of the current Python executable.
    """
    if not sys.executable:
        raise RuntimeEnvironmentError(
            "Failed to retrieve the path for the Python executable binary"
        )
    return sys.executable


class RuntimeEnvironmentError(Exception):
    """The base exception class for bootstrap env excepitons"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def _remove_package_from_requirements(package_name, file_path='./requirements.txt'):
    """ this is hack when the robbie package gets auto-added to the requirements.txt file in the auto-capture dependencies mode """
    # Read the file
    file_found = False
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            file_found = True
    except FileNotFoundError as e:
        return

    # Write back all lines except the one with the package name
    if not file_found:
        return
    try:
        with open(file_path, 'w') as file:
            for line in lines:
                # if not line.strip().startswith(package_name):
                if not package_name in line:
                    file.write(line)
    except Exception as e:
        return
    
import yaml

# TODO: remove, not used
def _remove_package_from_conda_yaml(file_path, package_name, output_path=None):
    """
    Removes a specific package from the dependencies of a Conda YAML file.
    
    Args:
        file_path (str): The path to the Conda YAML file.
        package_name (str): The name of the package to remove.
        output_path (str, optional): The path to save the modified YAML file. 
                                     If None, it will overwrite the original file.
    """
    # Step 1: Load the YAML file
    with open(file_path, 'r') as file:
        conda_yaml = yaml.safe_load(file)
    
    # Step 2: Modify the dependencies
    dependencies = conda_yaml.get('dependencies', [])
    
    # Handle dependencies that may be listed as dictionaries (for pip) or strings
    new_dependencies = []
    for dep in dependencies:
        if isinstance(dep, str):  # e.g., 'numpy=1.21.0'
            if not dep.startswith(package_name + '=') and dep != package_name:
                new_dependencies.append(dep)
        elif isinstance(dep, dict) and 'pip' in dep:  # pip dependencies are listed as a dictionary
            pip_dependencies = dep.get('pip', [])
            filtered_pip_dependencies = [pip_dep for pip_dep in pip_dependencies if not pip_dep.startswith(package_name + '=') and pip_dep != package_name]
            if filtered_pip_dependencies:
                new_dependencies.append({'pip': filtered_pip_dependencies})
        else:
            new_dependencies.append(dep)
    
    # Step 3: Update the conda YAML content
    conda_yaml['dependencies'] = new_dependencies

    # Step 4: Write the updated YAML file
    if output_path is None:
        output_path = file_path  # Overwrite the original file if no output path is provided
    
    with open(output_path, 'w') as file:
        yaml.dump(conda_yaml, file)
    
    logger.debug(f"Package '{package_name}' removed successfully from {output_path}.")

    
def _build_job_args(
    rpv: str, 
    dependencies: str,
    mode: str = None,
    debug: str = None,
):
    """
    Builds the job arguments for the container runtime

    Args:
        mode (str): The type of command runner to use
            - CONDA_MODE: Conda job (Python or non-Python) with dependencies defined by .yml
            - PYTHON_MODE: Non-conda Python job with dependencies defined by .txt or auto-captured
            - GENERIC: Shells commands to run without regard for Python or Conda
        rpv (str): The Python version to use in the container
        dependencies (str): The path to the dependencies file
    """
    job_args = []
    if not mode == None: 
        if mode not in [CONDA_MODE, PYTHON_MODE, GENERIC_MODE]:
            raise ValueError(f"Invalid command runner type: {mode}")
        job_args = ["--mode", mode]

    job_args.extend(
        [
        "--client_python_version",
        RuntimeEnvironmentManager()._current_python_version(),
        ]
    )

    job_args.extend(
        [
        "--rpv",
        rpv,
        ]
    )

    job_args.extend(
        [
        "--client_robbie_pysdk_version",
        RuntimeEnvironmentManager()._current_robbie_pysdk_version(),
        ]
    )

    job_args.extend(
        [
         "--dependency_settings",
            _DependencySettings.from_dependency_file_path(
                dependencies
            ).to_string(),
        ]
    )
    # if running under a conda env, send that over to the job
    if os.getenv("CONDA_DEFAULT_ENV"):
        job_args.extend(["--local_conda_env", os.getenv("CONDA_DEFAULT_ENV")])


    return job_args

def _running_in_conda():
    return True if os.getenv("CONDA_DEFAULT_ENV") else False


def _is_python_package_in_conda_yaml(file_path: str) -> bool:
    try:
        # Load the YAML file
        with open(file_path, 'r') as file:
            conda_env = yaml.safe_load(file)

        # Check if 'dependencies' key is in the file
        dependencies = conda_env.get('dependencies', [])
        
        # Search for the python package in dependencies
        for dep in dependencies:
            # Dependencies can be either strings or dictionaries for pip packages
            if isinstance(dep, str) and dep.startswith("python"):
                return True
            elif isinstance(dep, dict) and "python" in dep.get("pip", []):
                return True

        # If no python package found
        return False

    except Exception as e:
        logger.debug(f"Error reading or parsing {file_path}: {e}")
        return False
    
    import yaml
from typing import Optional

def _get_python_version_from_conda_yaml(file_path: str) -> Optional[str]:
    try:
        # Load the YAML file
        with open(file_path, 'r') as file:
            conda_env = yaml.safe_load(file)

        # Check if 'dependencies' key is in the file
        dependencies = conda_env.get('dependencies', [])

        # Search for the python package in dependencies
        for dep in dependencies:
            # Dependencies can be strings or dictionaries for pip packages
            if isinstance(dep, str) and dep.startswith("python"):
                # Extract version if specified (e.g., "python=3.8")
                if "=" in dep:
                    return dep.split("=")[1]  # Returns the version part
                else:
                    return "Version not specified"
            elif isinstance(dep, dict) and "pip" in dep:
                # Check pip dependencies
                for pip_dep in dep["pip"]:
                    if pip_dep.startswith("python"):
                        if "==" in pip_dep:
                            return pip_dep.split("==")[1]
                        else:
                            return "Version not specified"

        # Return None if no Python package is found
        return None

    except Exception as e:
        logger.debug(f"Error reading or parsing {file_path}: {e}")
        return None
    
        






