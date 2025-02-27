import os
from typing import Any
from .s3_client import get_s3_client
from .runner_env import runner_env
from .cloud_logger import logger

class CloudStorageClient:
    """Client for interacting with cloud storage. Abstracts S3 out."""
    def __init__(self):
        self.s3_client = get_s3_client()

    def download_file(self, s3_key: str, local_path: str):
        """Download a file from S3"""
        # ensure the local directory exists
        local_dir = os.path.dirname(local_path)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        try:
            self.s3_client.download_file(runner_env.S3_BUCKET, s3_key, local_path)
            logger.debug(f"Downloaded {s3_key} from S3 to {local_path}")
        except Exception as e:
            logger.error(f"Failed to download {s3_key} from S3: {e}")

    def get_object(self, s3_key: str) -> Any:
        """Get the contents of an S3 object into memory and return"""
        # TODO: may be used...
        try:
            response = self.s3_client.get_object(Bucket=runner_env.S3_BUCKET, Key=s3_key)
            return response['Body'].read()
        except Exception as e:
            logger.error(f"Failed to get {s3_key} from S3: {e}")
            raise

    def upload_file(self, local_path: str, s3_key: str):
        """Upload a file to S3"""
        bucket_name = runner_env.S3_BUCKET
        try:
            self.s3_client.upload_file(local_path, bucket_name, s3_key)
            logger.info(f"Uploaded {local_path} to S3 at {s3_key}")
        except Exception as e:
            logger.error(f"Failed to upload {local_path} to S3: {e}")
            raise

cloud_storage = CloudStorageClient()
