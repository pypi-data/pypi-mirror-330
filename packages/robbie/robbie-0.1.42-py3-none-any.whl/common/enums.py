from enum import Enum

# Cross component enums
log_types = dict(
    stdout="INFO",
    stderr="ERROR",
    debug="DEBUG"
)

class S3_CONSTANTS:
    FUNCTION_FOLDER = "function"
    SERIALIZED_FUNCTION_FILENAME = "function.pkl"
    SERIALIZED_ARGS_FILENAME = "args.pkl"
    SERIALIZED_KWARGS_FILENAME = "kwargs.pkl"
    RESULTS_FOLDER = "result"
    FUNCTION_RESULT_FILENAME = "result.pkl"
    FUNCTION_EXCEPTION_FILENAME = "exception.pkl"
    RESULTS_METADATA_FILENAME = "results_metadata.json"
    METADATA_FILENAME = "metadata.json"


class JobStatus(str, Enum):
    pending="pending"
    uploading="uploading"
    in_queue="in_queue"
    launching="launching_pod"
    pulling_image="pulling_image"
    pulled_image="pulled_image"
    starting_container="starting_container"
    started_container="started_container"
    initializing="initializing"
    computing="computing"
    storing="storing"
    complete="complete"
    failed="failed"
    execution_error="execution_error"
    terminate="terminate_job"
    terminated="terminated"

finished_job_statuses = {JobStatus.complete, JobStatus.execution_error, JobStatus.terminated, JobStatus.failed}
failed_job_statuses = {JobStatus.failed, JobStatus.execution_error, JobStatus.terminated}

class JobRunType(Enum):
    BASH_COMMAND_RUNNER = 'BASH_COMMAND_RUNNER'
    REMOTE_FUNCTION_CALL = 'REMOTE_FUNCTION_CALL'


