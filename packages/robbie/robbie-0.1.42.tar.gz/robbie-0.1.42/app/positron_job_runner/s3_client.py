# TODO: move this file to common
import boto3
from botocore.client import BaseClient
from .runner_env import runner_env

def get_s3_client() -> BaseClient:
    # Get the ROBBIE_RUNNER-prefixed credentials if they exist - this avoids breaking dev workflows
    robbie_access_key_id = runner_env.AWS_ACCESS_KEY_ID
    robbie_secret_access_key = runner_env.AWS_SECRET_ACCESS_KEY

    # Initialize S3 client
    if robbie_access_key_id and robbie_secret_access_key:
        # If the ROBBIE_RUNNER-prefixed credentials exist, use them
        session = boto3.Session(
            aws_access_key_id=robbie_access_key_id,
            aws_secret_access_key=robbie_secret_access_key
        )
        return session.client('s3', region_name=runner_env.REGION)
    # If ROBBIE_RUNNER-prefixed credentials don't exist, use default credentials from environment
    return boto3.client('s3',region_name=runner_env.REGION)
