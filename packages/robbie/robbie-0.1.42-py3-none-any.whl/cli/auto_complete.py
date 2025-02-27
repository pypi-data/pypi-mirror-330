import typer
from cli.helpers import (
    FundingSources,
    Environments,
    Images,
)
from cli.interactive import _get_files_with_extensions
from common.utils import is_valid_uuid
from positron_job_runner.runtime_environment_manager import (
    _running_in_conda,
    RuntimeEnvironmentManager
)

from rich.console import Console
err_console = Console(stderr=True)   
 # err_console.print(f"ctx.params={ctx.params}") 

"""
Auto complete functions for the `robbie run` command

These implement Typer specific autocompletion logic

https://typer.tiangolo.com/tutorial/options-autocompletion/#access-other-cli-parameters-with-the-context

"""
def job_config_auto_complete(ctx: typer.Context):
    """
    Job config for the CLI autocomplete
    """
    jc_files = _get_files_with_extensions(".", [".yaml"])
    return jc_files

def cluster_auto_complete(ctx: typer.Context):
    """
    cluster CLI autocomplete
    """
    return ["NERC", "EKS"]
    
def funding_group_auto_complete(ctx: typer.Context):
    """
    Funding groups for the CLI autocomplete
    """
    # check if `--environment_id` was already specified
    env = ctx.params.get('environment_arg')
    if (env):
        err_console.print(f"Error: please specify --funding-group first")
        return []
    try:
        fs = FundingSources.load()
        if fs == None:
            return []
        else:
            return fs.auto_complete_items()
    except Exception as e:
        err_console.print(f"[bold red]Auto complete error: {e}") 
        return [" "]
    
def environment_auto_complete(ctx: typer.Context):
    """
    Environments for the CLI autocomplete
    """
    fga = ctx.params.get('funding_arg')
    if (fga):
        # --funding_arg was previously specified
        try:
            envs = Environments.load(fga)
            if envs == None:
                err_console.print(f"Error: There are no environments in group: {fga}.")
                return []
            else:
                return envs.auto_complete_items()
        except Exception as e:
            err_console.print(f"[bold red]Auto complete error: {e}") 
            return [" "]
    else:
        # get the default FG
        try:
            fs = FundingSources.load()
            if fs == None:
                err_console.print(f"Error: Your are not a member of a Group")
                return []
            else:
                envs = Environments.load(fs.default_funding_source_id())
                if envs == None:
                    err_console.print(f"Error: Your have no enviroments in your Personal group.")
                    return []
                else:
                    return envs.auto_complete_items()
        except Exception as e:
            err_console.print(f"[bold red]Auto complete error: {e}") 
        return [" "]
    
    
def images_auto_complete(ctx: typer.Context):
    """
    Images for the CLI autocomplete
    """
    env = ctx.params.get('environment_arg')
    fg = ctx.params.get('funding_arg')
    if fg and env:
        try:
            images = Images.load(fg, env)
            if images == None:
                err_console.print(f"Error: No images are available.")
                return []
            else:
                img_list = images.auto_complete_items()
                img_list.append("auto-select")
                return img_list
        except Exception as e:
            err_console.print(f"[bold red]Auto complete error: {e}") 
        return [" "]
    
def deps_auto_complete(ctx: typer.Context):
    """
    Dependencies autocomplete
    """
    ca = ctx.params.get('conda_arg')
    if ca:
        conda_env_list = _get_files_with_extensions(".", [".yml", ".yaml"])
        if _running_in_conda():
            conda_env_list.extend([f"auto-capture"])
        return conda_env_list

    pv = ctx.params.get('python_ver_arg')
    pa = ctx.params.get('python_arg')
    if pv and not pa:
        err_console.print(f"[bold red]Can't specify version, specifying --python first")
        return [" "] 
    if pa:
        py_deps_list = _get_files_with_extensions(".", [".txt"])
        if pv:
            if pv == RuntimeEnvironmentManager()._current_python_version():
                py_deps_list.extend(
                        ["auto-capture", 
                        "none"]
            )
            else:
                py_deps_list.extend(["none"])
        else:
            py_deps_list.extend(
                ["auto-capture", 
                "none"]
            )
        return py_deps_list

    return [" "]
    
def set_env_auto_complete():
    return ["local", "dev", "alpha", "beta"]


def jobs_auto_complete(incomplete: str):
    from cli.cmds.download import Jobs
    try:
        jobs = Jobs.load()
        if (jobs):
            completion = []
            # returns list of tuples (name, id)
            for name in jobs.auto_complete_items():
                if name[0].startswith(incomplete):
                    completion.append(name)
            return completion
    except Exception as e:
        err_console.print(f"[bold red]Auto complete error: {e}") 
        return [" "]

    