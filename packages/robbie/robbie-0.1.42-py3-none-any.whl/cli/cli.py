import typer
from cli.cmds.run import run
from cli.cmds.login import login
from cli.cmds.set_env import set_env
from cli.cmds.config import config
from cli.cmds.download import download
from cli.cmds.set_log_level import log_level
from cli.cmds.version import version
from cli.cmds.cmd_dump import dump
from cli.cmds.get import get
from cli.cmds.kill import kill
from cli.cmds.delete import delete
from cli.cmds.pd import pd
from cli.cmds.rec import rec

app = typer.Typer(help="A CLI tool to help you run your code in the Robbie")

app.command()(dump)
app.command()(run)
app.command()(login)
app.command()(set_env)
app.command()(config)
app.command()(download)
app.command()(version)
app.command()(get)
app.command()(kill)
app.command()(delete)
app.command()(pd)
app.command()(rec)
app.callback()(log_level)

if __name__ == "__main__":
    app()
