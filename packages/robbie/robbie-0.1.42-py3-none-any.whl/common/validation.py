from typing import Optional
from common.console import console
from common.utils import _current_python_version

def validate_python_version(image: Optional[str]) -> bool:
    # example python version: 3.12
    # example image: robbie:1.0.0-gpu-py3.12-torch2.5-ubuntu22.04-dev
    if image:
        image_python_version = image.split("-")[2].replace("py", "")
        python_version = _current_python_version()
        if image_python_version != python_version:
            console.print(f"[red]Error: Python version mismatch. The image you are using is built for Python {image_python_version}, but you are running Python {python_version}[/red]")
            return False
    return True

def warn_python_version(image: Optional[str]):
    # example python version: 3.12
    # example image: robbie:1.0.0-gpu-py3.12-torch2.5-ubuntu22.04-dev
    if image:
        if image == "condatest:latest":
            print("Skipping python version check for condatest image")
            return
        image_python_version = image.split("-")[2].replace("py", "")
        python_version = _current_python_version()
        if image_python_version != python_version:
            console.print(f"[yellow]Warning: Python version mismatch. The image you are using is built for Python {image_python_version}, but you are running Python {python_version}[/yellow]")
