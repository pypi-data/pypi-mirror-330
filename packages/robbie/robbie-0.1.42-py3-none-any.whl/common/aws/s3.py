import requests

from common.env_config import env
from common.api.presigned_url import (
    get_upload_presigned_url,
    get_download_presigned_url
)
from common.exceptions import RemoteCallException, DecoratorException
from ..logging_config import logger



class S3Uploader():
    """This class is responsible for handling file transfer 
       to and from Amazon S3 trough presigned URLs."""

    @staticmethod
    def upload_bytes(bytes, job_id, path):
        presigned_resp = get_upload_presigned_url(job_id, path)
        
        filename = path.split('/')[-1]
        # Create a file-like object from bytes
        files = {'file': (filename, bytes)}
        response = requests.post(presigned_resp.get('url'), data=presigned_resp.get('fields'), files=files) 
        if response.status_code != 204:
            raise DecoratorException(
                f'Upload failed with http code: {response.status_code} \n {response.text}')
            

    @staticmethod
    def upload_file(file_path, job_id, path):
        presigned_resp = get_upload_presigned_url(job_id, path)

        with open(file_path, 'rb') as f:
            files = {'file': (path, f)}
            response = requests.post(presigned_resp.get('url'), data=presigned_resp.get('fields'), files=files)
            logger.debug(response)
            if response.status_code != 204:
                raise DecoratorException(
                    f'Upload failed with http code: {response.status_code} \n {response.text}')

class S3Downloader():
    """This class is responsible for handling file transfer 
       to and from Amazon S3 trough presigned URLs."""
    @staticmethod
    def download_file_to_bytes(job_id, file_path):
        presigned_resp = get_download_presigned_url(job_id, file_path)
        resp = requests.get(presigned_resp.get('url'))
        if resp.status_code != 200:
            return None
        else:
            return resp.content


   