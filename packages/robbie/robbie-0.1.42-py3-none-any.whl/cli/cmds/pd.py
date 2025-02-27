import os
import sys
import typer
import platform
import subprocess
import select
import threading
import boto3
import time
import awscli.clidriver
from awscli.testutils import create_clidriver
from typing import Optional, List
from typing_extensions import Annotated
from common.api.get_pd_auth import get_pd_auth
from common.observability.main import track_command_usage
from common.env_defaults import current
from common.console import console
from cli.cmds.login import login
from common.logging_config import logger


@track_command_usage("pd")
def pd(
  command: Annotated[str, typer.Argument(help='Peristent disk operation: ls, cp, mv, rm, mkdir')],
  arg_1: Annotated[Optional[str], typer.Argument(help='Argument 1')] = None,
  arg_2: Annotated[Optional[str], typer.Argument(help='Argument 2')] = None,
  recursive: Annotated[bool, typer.Option("--recursive", help='Recursively operate on files')] = False,
  exclude: Annotated[List[str], typer.Option("--exclude", help='Exclude specific files/regex')] = None,
  include: Annotated[List[str], typer.Option("--include", help='Includes specific files/regex')] = None,
  dryrun: Annotated[bool, typer.Option("--dryrun", help='Dry run the command')] = False
):
    """
    Persistent disk operations: ls, cp, mv, rm, mkdir
    """
    login()

    # what stage are we using?
    stage = current.name
    logger.debug(f"Current stage: {stage}")

    try:
        result = get_pd_auth()
        identity_id = result['identityId']
        user_email = result['userEmail']
        logger.debug(f"Retrieved Identity ID: {identity_id}")
        logger.debug(f"User Email: {user_email}")
        #print(f"Retrieved Identity ID: {identity_id}")

        # Initialize the Cognito Identity client
        client = boto3.client('cognito-identity', region_name='us-west-2')  # Change region as needed

        logger.debug(f"Getting AWS credentials for identity:{identity_id}")
        response = client.get_credentials_for_identity(
            IdentityId=identity_id
        )
        credentials = response['Credentials']
        if not credentials:
            console.print("Error: Unable to retrieve AWS credentials")
            return

        logger.debug(f"Temporary AWS Credentials:{credentials}") 

        os.environ['AWS_ACCESS_KEY_ID'] = credentials['AccessKeyId']
        os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['SecretKey']
        os.environ['AWS_SESSION_TOKEN'] = credentials['SessionToken']
        os.environ['AWS_DEFAULT_REGION'] ="us-west-2"

        if command not in [ "ls", "cp", "mv", "rm", "mkdir"]:
            console.print("Error: Invalid persistent disk command")
            return

        # users have permission to read/write to their own persistent disk
        pd_base = f"s3://positron-{stage}-workspaces/{user_email}/persistent-job-disk/"

        # are we dry running?
        if dryrun:
            dr = " --dryrun"
        else:
            dr = ""

        # are we do a recursive operation?
        if recursive:
            rec = " --recursive"
        else:
            rec = ""

        # process one or more excludes
        excl = ""
        if exclude:
            for e in exclude:
                excl += f" --exclude {e}"

        # process one or more includes
        incl = ""
        if include:
            for i in include:
                incl += f" --include {i}"   

        # list the contents of the persistent disk/directory
        if command == "ls":
            if arg_1:
                if not arg_1.startswith("pd://"):
                    console.print("Error: rm requires an `pd` location.")
                    return
                arg_1_full = f'{pd_base}{arg_1.removeprefix("pd://")}'
                command = f"aws s3 ls {arg_1_full}{rec}{dr} --human-readable --summarize"
            else:
                command = f"aws s3 ls {pd_base}{rec}{dr} --human-readable --summarize"

        # copy files to/from the persistent disk
        if command == "cp":
            if not arg_1 or not arg_2:
                console.print("Error: cp requires two arguments.")
                return

            # if is an S3 location, expand the path 
            if arg_1.startswith("pd://"):
                arg_1_full = f'{pd_base}{arg_1.removeprefix("pd://")}'
            else:
                arg_1_full = arg_1

            # if is an S3 location, expand the path    
            if arg_2.startswith("pd://"):
                arg_2_full = f'{pd_base}{arg_2.removeprefix("pd://")}'
            else:
                arg_2_full = arg_2

            command = f"aws s3 cp {arg_1_full} {arg_2_full}{incl}{excl}{rec}{dr}"

        # move files to/from the persistent disk
        if command == "mv":
            if not arg_1 or not arg_2:
                console.print("Error: mv requires two arguments.")
                return

            # if is an S3 location, expand the path 
            if arg_1.startswith("pd://"):
                arg_1_full = f'{pd_base}{arg_1.removeprefix("pd://")}'
            else:
                arg_1_full = arg_1

            # if is an S3 location, expand the path    
            if arg_2.startswith("pd://"):
                arg_2_full = f'{pd_base}{arg_2.removeprefix("pd://")}'
            else:
                arg_2_full = arg_2

            command = f"aws s3 mv {arg_1_full} {arg_2_full}{incl}{excl}{rec}{dr}"
        
        # create a new directory on the persistent disk
        if command == "mkdir":
            if not arg_1:
                console.print("Error: mkdir requires one argument.")
                return
            if not arg_1.startswith("pd://"):
                console.print("Error: mkdir requires an `pd://` location.")
                return
            if recursive:
                console.print("Error: mkdir doesn't support the --recursive option.")
                return
            if arg_2:
                console.print("Error: mkdir doesn't a second argument.")
                return
            if include or exclude:
                console.print("Error: mkdir support --include or --exclude options.")
                return

            # just strip off the pd:// prefix
            arg_1_full = arg_1.removeprefix("pd://")
            command = f"aws s3api put-object --bucket positron-{stage}-workspaces --key {user_email}/persistent-job-disk/{arg_1_full}/{dr}"

        if command == "rm":
            if not arg_1:
                console.print("Error: rm requires one argument.")
                return
            if not arg_1.startswith("pd://"):
                console.print("Error: rm requires an a `pd://` location.")
                return
            if arg_2:
                console.print("Error: rm doesn't a second argument.")
                return
            if arg_1.endswith("persistent-job-disk") or arg_1.endswith("persistent-job-disk/"):
                console.print("Error: Cannot delete the root directory.")
                return
            if recursive:
                rec = " --recursive"
            else:
                rec = ""
            
            arg_1_full = f'{pd_base}{arg_1.removeprefix("pd://")}'
            command = f"aws s3 rm {arg_1_full}{incl}{excl}{rec}{dr}"

        if not command:
            console.print("Error: no command to run")
            return

        cmd_list = command.split()
        if not isinstance(cmd_list, list):
            console.print("Error: Command must be a list")
            return
        
        # override sys.argv to pass these arguments to awscli driver (function)
        sys.argv = cmd_list
        logger.debug(f"new sys.argv:{sys.argv}")
        # call the library directly. This eliminates the need to call the awscli command from the shell
        return_code = awscli.clidriver.main()
        if return_code == 0:
            console.print("SUCCESS")
        else:
            console.print(f"ERROR: {return_code}")
        return
    
    except Exception as e:
        console.print(f"Error running command: {e}")
        return



