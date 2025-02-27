import boto3
from botocore.client import BaseClient
from .runner_env import runner_env

def create_client() -> BaseClient:
    robbie_access_key_id = runner_env.AWS_ACCESS_KEY_ID
    robbie_secret_access_key = runner_env.AWS_SECRET_ACCESS_KEY

    # Initialize CloudWatch client
    if robbie_access_key_id and robbie_secret_access_key:
      # If the ROBBIE_RUNNER-prefixed credentials exist, use them
        session = boto3.Session(
            aws_access_key_id=robbie_access_key_id,
            aws_secret_access_key=robbie_secret_access_key
        )
        return session.client('logs', region_name=runner_env.REGION)
    
    return boto3.client('logs', region_name=runner_env.REGION)
