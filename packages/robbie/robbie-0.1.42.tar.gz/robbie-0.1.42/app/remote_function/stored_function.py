from typing import Any, Callable, Dict, Tuple, Union
from common.aws.s3 import (
    S3Uploader,
    S3Downloader
)
from remote_function.meta_data import MetaData, FunctionHashes
from remote_function.img_result import ImageResult
from common.utils import is_notebook
from remote_function.serializer import Serializer
from common.enums import S3_CONSTANTS

class StoredFunction():
    func: Callable[[], str]
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]
    result: Union[Any, None] = None
    exception: Union[Exception, None] = None
    result_meta: Union[MetaData, None] = None
    s_func: bytes
    s_args: bytes
    s_kwargs: bytes
    s_result: bytes
    s_exception: bytes
    s_meta: MetaData
    job_id: str = ""
    base_dir: str

    def __init__(self, func = None, args = None, kwargs = None) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs


    def serialize_function(self):
        self.s_func = Serializer.serialize(self.func)
        self.s_args = Serializer.serialize(self.args)
        self.s_kwargs = Serializer.serialize(self.kwargs)


    def create_function_metadata(self, hmac_key: str):
        self.s_meta = MetaData(sha256_hash=FunctionHashes(
            func_hash=Serializer.compute_hash(self.s_func, hmac_key),
            args_hash=Serializer.compute_hash(self.s_args, hmac_key),
            kwargs_hash=Serializer.compute_hash(self.s_kwargs, hmac_key),
        ))


    def deserialize_function(self):
        self.func = Serializer.deserialize(self.s_func)
        self.args = Serializer.deserialize(self.s_args)
        self.kwargs = Serializer.deserialize(self.s_kwargs)


    def serialize_results(self):
        if self.result is not None:
            self.s_result = Serializer.serialize(self.result)
        if self.exception is not None:
            self.s_exception = Serializer.serialize(self.exception)


    def create_results_metadata(self, hmac_key: str):
        sha256_hash=FunctionHashes()
        if self.result is not None:
            sha256_hash.result_hash = Serializer.compute_hash(self.s_result, hmac_key)
        if self.exception is not None:
            sha256_hash.exception_hash = Serializer.compute_hash(self.s_exception, hmac_key)

        self.s_meta = MetaData(sha256_hash=sha256_hash)


    def set_job_id(self, job_id: str):
        self.job_id = job_id


    def upload_to_s3(self):
        func_path = f"{S3_CONSTANTS.FUNCTION_FOLDER}/{S3_CONSTANTS.SERIALIZED_FUNCTION_FILENAME}"
        args_path = f"{S3_CONSTANTS.FUNCTION_FOLDER}/{S3_CONSTANTS.SERIALIZED_ARGS_FILENAME}"
        kwargs_path = f"{S3_CONSTANTS.FUNCTION_FOLDER}/{S3_CONSTANTS.SERIALIZED_KWARGS_FILENAME}"
        meta_path = f"{S3_CONSTANTS.FUNCTION_FOLDER}/{S3_CONSTANTS.METADATA_FILENAME}"
        S3Uploader.upload_bytes(self.s_func, self.job_id, func_path)
        S3Uploader.upload_bytes(self.s_args, self.job_id, args_path)
        S3Uploader.upload_bytes(self.s_kwargs, self.job_id, kwargs_path)
        S3Uploader.upload_bytes(self.s_meta.to_json(), self.job_id, meta_path)


    def run(self):
        """Runs the function and stores the result"""
        try:
            self.result = self.func(*self.args, **self.kwargs)
        except Exception as e:
            self.exception = e


    def load_and_validate_results(self, hmac_key: str):
        image_result = ImageResult(self.job_id)
        if is_notebook() and image_result.has_images():
            image_result.show_images()

        try:
            function_result_path = f"{S3_CONSTANTS.RESULTS_FOLDER}/{S3_CONSTANTS.FUNCTION_RESULT_FILENAME}"
            function_exception_path = f"{S3_CONSTANTS.RESULTS_FOLDER}/{S3_CONSTANTS.FUNCTION_EXCEPTION_FILENAME}"
            result_metadata_path = f"{S3_CONSTANTS.RESULTS_FOLDER}/{S3_CONSTANTS.RESULTS_METADATA_FILENAME}"
            self.s_result = S3Downloader.download_file_to_bytes(self.job_id, function_result_path)
            self.s_exception = S3Downloader.download_file_to_bytes(self.job_id, function_exception_path)
            result_meta = S3Downloader.download_file_to_bytes(self.job_id, result_metadata_path)
            self.result_meta = MetaData.from_json(result_meta)
            self._validate_result_meta(hmac_key)
            self.result = Serializer.deserialize(self.s_result) if self.s_result is not None else None
            self.exception = Serializer.deserialize(self.s_exception) if self.s_exception is not None else None
        except Exception as e:
            self.exception = e
        return self.result, self.exception

    def _validate_result_meta(self, hmac_key: str):
        result_computed_hash = Serializer.compute_hash(self.s_result, hmac_key)
        exception_computed_hash = Serializer.compute_hash(self.s_exception, hmac_key)
        if (self.s_result):
            if self.result_meta.sha256_hash.get('result_hash') != result_computed_hash:
                raise Exception('Integrity check of result files failed. Ensure no one has access to your cloud storage.')
        if (self.s_exception):
            if self.result_meta.sha256_hash.get('exception_hash') != exception_computed_hash:
                raise Exception('Integrity check of result files failed. Ensure no one has access to your cloud storage.')

