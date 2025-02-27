import typer
from typing import Annotated
from .runner_env import runner_env # this order is important; needs to initialize POSITRON_CLOUD_ENVIRONMENT
from .run_job import run
from .cloud_logger import logger

app = typer.Typer(help="Runs your job in Project Robbie.")

@app.command()
def hello():
    """
    Describes what you can do with the Positron Job Runner
    """
    logger.info('Hello, I am the Robbie Job Runner')
    logger.info('Here is a list of things I can help you with:')
    logger.info('- Run a job in Project Robbie')

@app.command()
def run_job(
    rerun: Annotated[bool, typer.Option(help='Enables rerunning a job')] = False,
):
    """
    Run the job from inside a Positron container.

    Example usage:
    $ positron_job_runner run_job
    """
    # @TODO: Validate that all necessary env variables are correctly set (JOB_ID...)

    logger.info('Running job in Project Robbie')
    logger.info(f'Job ID: {runner_env.JOB_ID}')
    runner_env.rerun = rerun

    try:
        run()
    except Exception as e:
        logger.exception(e)
        exit(0)


if __name__ == "__main__":
    app()
