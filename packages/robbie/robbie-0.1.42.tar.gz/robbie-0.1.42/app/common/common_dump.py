import sys
import os
import subprocess
import platform
import psutil
from common.console import console, print_boxed_messages
from common.build_env import build_env
from common.utils import get_version
from common.env_defaults import current
from common.env_config import env
from common.user_config import user_config
from common.config import (
    load_job_config, 
    PositronJob
)
from common.cli_args import args
from common.api.validate_user_auth_token import is_auth_token_valid
from positron_job_runner.runtime_environment_manager import RuntimeEnvironmentManager, _DependencySettings, _python_executable

def common_dump(
    machine: bool = None,
    conda: bool = None,
    python: bool = None,
    sdk: bool = None,
    job_config: bool = None,
    job_config_name: str = "./job_config.yaml",
    save: bool = None
):

    def dump_machine():
        my_system = platform.uname()

        # Print the information
        my_info = f"System: {my_system.system}\n"
        my_info += f"Node Name: {my_system.node}\n"
        my_info += f"Release: {my_system.release}\n"
        my_info += f"Version: {my_system.version}\n"
        my_info += f"Machine: {my_system.machine}\n"
        my_info += f"Processor: {my_system.processor}\n"
        # Get CPU information
        my_info += f"CPU Count: {psutil.cpu_count(logical=False)}\n"
        my_info += f"CPU Usage: {psutil.cpu_percent(interval=1)}%\n"

        # Get memory information
        mem = psutil.virtual_memory()
        my_info += f"Total Memory: {mem.total / (1024.0 ** 3):.2f} GB\n"
        my_info += f"Available Memory: {mem.available / (1024.0 ** 3):.2f} GB\n"

        # Get disk information
        disk = psutil.disk_usage('/')
        my_info += f"Total Disk Space: {disk.total / (1024.0 ** 3):.2f} GB\n"
        my_info += f"Used Disk Space: {disk.used / (1024.0 ** 3):.2f} GB\n"

        print_boxed_messages("Local Machine Info", my_info)

    def dump_conda():
        console.print("Dumping Conda environment")

        is_conda_installed = False
        try:
            RuntimeEnvironmentManager()._get_conda_exe()
            is_conda_installed = True
        except ValueError as e:
           console.print(f"[red]No Conda/mamba executable not found: {str(e)}")

        # sanity checks
        if not is_conda_installed and os.getenv("CONDA_DEFAULT_ENV"):
            console.print(f"No Conda executable found but you are running in a Conda environment({RuntimeEnvironmentManager._get_active_conda_env_name()})")
            return
    
        if is_conda_installed and not os.getenv("CONDA_DEFAULT_ENV"):
            console.print(f"Conda executable found but you are not running in a conda environment (it's OK)")
            return

        if is_conda_installed and os.getenv("CONDA_DEFAULT_ENV"):
            result = subprocess.run("conda info", capture_output=True, shell=True, text=True)
            print_boxed_messages(f'conda info', result.stdout)

            title = f"Conda environment detected: {RuntimeEnvironmentManager()._get_active_conda_env_name()}"
            py_env = f'CONDA_DEFAULT_ENV (active): {RuntimeEnvironmentManager()._get_active_conda_env_name()}\n'
            py_env += f'CONDA_PREFIX: {RuntimeEnvironmentManager()._get_active_conda_env_prefix()}\n'
            py_env += f'conda_executable: {RuntimeEnvironmentManager()._get_conda_exe()}\n'
            try:
                py_conda = RuntimeEnvironmentManager()._python_version_in_conda_env(os.getenv("CONDA_DEFAULT_ENV"))
                py_env += f'python_version_in_conda_env: {py_conda}\n'
            except Exception as e:
                py_env += f'python_version_in_conda_env: Python not found\n'

            py_env = f'Python executable (sys.executable): {sys.executable}\n'
            py_env += f'Python executable (os.__file__): {os.__file__}\n'
            py_env += f'current_python_version: {RuntimeEnvironmentManager()._current_python_version()}\n'

            print_boxed_messages(f'({title})', py_env)

            result = subprocess.run("conda list", capture_output=True, shell=True, text=True)
            print_boxed_messages(f'Installed Python Packages (% conda list)', result.stdout)

            result = subprocess.run("conda config --show", capture_output=True, shell=True, text=True)
            print_boxed_messages(f'Conda configuration (% conda config --show)', result.stdout)

            # result = subprocess.run("conda env export", capture_output=True, shell=True, text=True)
            # print_boxed_messages("% conda env export", result.stdout)

            result = subprocess.run("conda env export --from-history", capture_output=True, shell=True, text=True)
            print_boxed_messages("% conda env export --from-history", result.stdout)

            # Try to capture dependencies from the conda environment, if any.
            conda_env_prefix = RuntimeEnvironmentManager()._get_active_conda_env_prefix()
            local_dependencies_path = os.path.join(os.getcwd(), "dumped_environment.yml")
            RuntimeEnvironmentManager()._export_conda_env_from_prefix(conda_env_prefix, local_dependencies_path)
            
            try:
                with open(local_dependencies_path, 'r') as file:
                    # Read the content of the file
                    file_content = file.read()
                    print_boxed_messages(f"Platform-specific: ({platform.system()}) export: {local_dependencies_path}", file_content)
            except Exception as e:
                console.print(f'[red]Failed to open: {local_dependencies_path}')

    def dump_python():
        console.print("Dumping Python environment")
        py_env = f'Python executable (sys.executable): {sys.executable}\n'
        py_env += f'Python executable (os.__file__): {os.__file__}\n'
        py_env += f'current_python_version: {RuntimeEnvironmentManager()._current_python_version()}\n'
    
        if not os.getenv("CONDA_DEFAULT_ENV"):
            print_boxed_messages("Non-Conda Conda environment detected", py_env)
            if platform.system() == 'Windows':
                result = subprocess.run("where python", capture_output=True, shell=True, text=True)
                print_boxed_messages('Python local (% where python)', result.stdout)
            else:   
                result = subprocess.run("which python", capture_output=True, shell=True, text=True)
                print_boxed_messages('Python local (% which python)', result.stdout)
            result = subprocess.run("pip list", capture_output=True, shell=True, text=True)
            print_boxed_messages('Installed Python Packages (% pip list)', result.stdout)

            # show the auto-capture output into requirements.txt
            RuntimeEnvironmentManager()._capture_from_pip_runtime(output_file="dump_requirements.txt")
            try:
                with open("dump_requirements.txt", 'r') as file:
                    # Read the content of the file
                    file_content = file.read()
                    print_boxed_messages(f"Auto-captured dump_requirements.txt", file_content)
            except Exception as e:
                console.print(f"[red]Failed to open: 'dump_requirements.txt'")
        else:
            console.print("[red]Conda environment detected, skipping Python local details. Run `robbie dump --conda` to see Conda details")

    def dump_sdk():
        console.print("Dumping SDK environment")
        # now dump everything related to the Robbie SDK version
        rob_ver = f'current_robbie_pysdk_version: {RuntimeEnvironmentManager()._current_robbie_pysdk_version()}\n'
        result = subprocess.run("pip show robbie", capture_output=True, shell=True, text=True)
        rob_ver += f"Robbie SDK version (% pip show robbie): {result.stdout}"
        rob_ver += f"Robbie Python SDK version - importlib.metadata.version('robbie'): {get_version()}"
        print_boxed_messages("Robbie Version Details", rob_ver)

        # dump the SDK environment
        print_boxed_messages("build_env", str(build_env))
        print_boxed_messages("EnvConfig (env)", env.to_string())
        print_boxed_messages("EnvDefaults (current)", current.to_string())
        print_boxed_messages("User Config (user_config)", user_config.to_string())     
        print_boxed_messages("CLI Arguments (args)", args.to_string())

        print_boxed_messages("API Test", api_test())

    def dump_job_config(
        dump: bool,
        name: str = None
    ):

        if dump == False:
            return

        if name == None:
            name = "./job_config.yaml"

        console.print(f"Dumping Job Config: {name}")
        try:
            global_job_config_yaml = load_job_config(name)
        except Exception as e:
            print(f"Error loading job configuration: {name} {str(e)}")
            global_job_config_yaml = None
    
        if global_job_config_yaml:
            print_boxed_messages(f"{name} contents:", global_job_config_yaml.to_string())

            if global_job_config_yaml.include_local_dir:
                contents = os.listdir(os.getcwd())
                print_boxed_messages('CWD (os.getcwd()) contents', "\n".join(contents))

            if global_job_config_yaml.dependencies and global_job_config_yaml.dependencies != "none":

                # return the file name or auto-capture
                try:
                    dep_file = RuntimeEnvironmentManager().snapshot(global_job_config_yaml.dependencies)

                    if os.path.exists(dep_file):
                        try:
                            with open(dep_file, 'r') as file:
                                # Read the content of the file
                                file_content = file.read()
                                print_boxed_messages(f'global_job_config_yaml.dependencies: {global_job_config_yaml.dependencies}, file: {dep_file}', file_content)
                        except Exception as e:
                            console.print(f'[red]Failed to open: global_job_config_yaml.dependencies: {dep_file}')
                    else:
                        console.print(f'[red]global_job_config_yaml.dependencies file: {dep_file} does not exist')
                except Exception as e:
                    console.print(f'[red]Error capturing dependencies: {str(e)}')
        

    if machine:
        dump_machine()
    if conda:
        dump_conda()
    if python:
        dump_python()
    if sdk:
        dump_sdk()
    if job_config:
        dump_job_config(job_config, job_config_name)

    # print(f"machine: {machine}, conda: {conda}, python: {python}, sdk: {sdk}, job_config: {job_config}, job_config_name: {job_config_name}")

    flag = machine or conda or python or sdk or job_config
    if not flag and job_config_name:
        console.print(f"[red]Error: job_config_name: {job_config_name} provided but no other flags set. Did you mean --conda or --python?")
    elif not flag:
        dump_machine()
        if os.getenv("CONDA_DEFAULT_ENV"):
            dump_conda()
        else:
            dump_python()
        dump_sdk()
        dump_job_config(job_config, job_config_name)

    print_boxed_messages("End of Robbie local environment dump", "That's all folks!")


def dump_data():
    """All the same data as common_dump, but returned as a dict"""
    fake_job_config = False
    try:
        job_config = load_job_config()
        if not job_config:
            fake_job_config = True
            job_config = PositronJob()
            job_config.dependencies = None
    except Exception as e:
        print(f'Error loading job configuration! {str(e)}')
        fake_job_config = False

    return {
        "Python executable (sys.executable)": sys.executable,
        "Python executable (os.__file__)": os.__file__,
        "Robbie Python SDK version - importlib.metadata.version('robbie')": get_version(),
        "Robbie SDK version (% pip show robbie)": subprocess.run("pip show robbie", capture_output=True, shell=True, text=True).stdout,
        "Installed Python Packages (% pip list)": subprocess.run("pip list", capture_output=True, shell=True, text=True).stdout,
        "./requirements.txt": open("./requirements.txt", 'r').read() if os.path.exists("./requirements.txt") else None,
        "./job_config.yaml": job_config.to_string() if not fake_job_config else "No job_config.yaml found",
        # "RuntimeEnvironmentManager": rtem_to_string(job_config),
        "build_env": str(build_env),
        "EnvConfig (env)": env.to_string(),
        "EnvDefaults (current)": current.to_string(),
        "User Config (user_config)": user_config.to_string(),
        "CLI Arguments (args)": args.to_string(),
    }

def api_test():
    try:
        result = is_auth_token_valid()
        return f"is_auth_token_valid(): API call - successful, result: {result}"
    except Exception as e:
        return f"is_auth_token_valid(): API call - failed: {str(e)}"

