import platform
from rich.console import Console
from rich import box
from rich.text import Text
from rich.panel import Panel

# Website colors
ROBBIE_BLUE='#41a7ff'
ROBBIE_DEFAULT='#ced7bd'
ROBBIE_ORANGE='#ff3a24'
ROBBIE_GREY='#f2f2f2'
ROBBIE_YELLOW='#f5f543'

# Used to print nice message to the end user, this is not a logger. See `logging_config.py` for logging.
console = Console()

def print_boxed_messages(title: str, message: str):
    """
    Prints a message in a box with a title.
    """
    text = Text()
    text.append(message)
    console.print(Panel(
        text,
        box=box.ROUNDED,
        # padding=(1, 2),
        title = Text(title, style=ROBBIE_BLUE),
        border_style=ROBBIE_ORANGE,
    ))
