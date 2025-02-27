from pydantic import BaseModel
from typing import List, Optional
from rich.text import Text
from common.console import console, print_boxed_messages
from common.utils import _exit_by_mode, FAILURE

class PositronCLIArgs(BaseModel):
    """
    Positron CLI command line arguments.
    """
    is_init: bool = False
    name: Optional[str] = None
    local: bool = False
    deploy: bool = False
    stream_stdout: bool = False
    job_args: Optional[List[str]] = None
    skip_prompts: bool = False
    commands_to_run: Optional[str] = None
    interactive: bool = False
    create_only: bool = False
    local_container: Optional[str] = None
    results_from_job_id: str = ""
    download: Optional[str] = None
    local_path: Optional[str] = None


    def init(self,
        name: Optional[str] = None,
        local: bool = False,
        deploy: bool = False,
        stream_stdout: bool = False,
        job_args: Optional[List[str]] = None,
        skip_prompts: bool = False,
        commands_to_run: Optional[str] = None,
        interactive: bool = False,
        create_only: bool = False,
        local_container: Optional[str] = None,
        results_from_job_id: str = "",
        download: Optional[str] = None,
        local_path: Optional[str] = None,
    ):
        if self.is_init:
            # raise ValueError('CLI Args already initialized')
            console.print('[red]ERROR, did you rerun your notebook without resetting the Kernel?')
            _exit_by_mode(FAILURE)
        
        self.name = name
        self.local = local
        self.deploy = deploy
        self.stream_stdout = stream_stdout
        self.job_args = job_args
        self.is_init = True
        self.skip_prompts=skip_prompts
        self.commands_to_run = commands_to_run
        self.interactive = interactive
        self.create_only = create_only
        self.local_container = local_container
        self.results_from_job_id = results_from_job_id
        self.download = download
        self.local_path = local_path

    def to_string(self, include_title: bool = False) -> str:
        message = f"""- name: {self.name}
- local: {self.local}
- deploy: {self.deploy}
- stream_stdout: {self.stream_stdout}
- job_args: {self.job_args}
- skip_prompts: {self.skip_prompts}
- commands_to_run: {self.commands_to_run}
- interactive: {self.interactive}
- create_only: {self.create_only}
- results_from_job_id: {self.results_from_job_id}
- download: {self.download}
- local_path: {self.local_path}
- is_init: {self.is_init}"""
        
        if include_title:
            return f"========== CLI Arguments (args) ==========\n{message}"
        else:
            return message

    


#
# Export global (singleton)
#
args = PositronCLIArgs()
"""
Global CLI arguments singleton, make sure you call init() before using it.
"""
