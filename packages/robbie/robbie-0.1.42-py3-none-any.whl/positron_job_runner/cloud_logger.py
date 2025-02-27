import json
import sys
import time
import logging
import threading
from logging import ERROR, INFO, DEBUG, WARNING
from positron_job_runner.runner_env import runner_env
from positron_job_runner.cloudwatch_client import create_client
from positron_job_runner.logging_config import get_logger

console_logger = get_logger()

class CloudLogger:
  """A class to log messages to stdout, stderr, and CloudWatch."""
  stdout = []
  stderr = []
  # cloudwatch_client = None

  def __init__(self):
    # Connect to cloudwatch if enabled
    if runner_env.AWS_JOB_LOG_GROUP_NAME:
      self.__cloudwatch_client = create_client()
      self._start_error_batch_thread()
    else:
      console_logger.info("CloudWatch logging is disabled.")

  def error(self, message: str):
    self.log(message, ERROR)

  def warning(self, message: str):
    self.log(message, WARNING)

  def info(self, message: str):
    self.log(message, INFO)
  
  def debug(self, message: str):
    self.log(message, DEBUG)
  
  def exception(self, *args, **kwargs):
    console_logger.exception(*args, **kwargs)
    self.log(str(args[0]), ERROR)

  def log(self, message: str, level = INFO):
    if isinstance(message, bytes):
        message = message.decode('utf-8')
    
    # Store in mem for later retrieval
    if level == ERROR:
        self.stderr.append(message)
    else:
        self.stdout.append(message)

    # Log to console at the provided level.
    console_logger.log(level = level, msg = message)

    # Log to CloudWatch if enabled and not an error (errors are batched)
    if runner_env.AWS_JOB_LOG_GROUP_NAME and level != ERROR:
      self._log_to_cloudwatch([message], level)

    # This ensures logs in the right order etc, but may slow down the process
    sys.stdout.flush()
    sys.stderr.flush()

  def end_of_logs_signal(self):
    if runner_env.AWS_JOB_LOG_GROUP_NAME:
      self._stop_event.set()
      self._batch_thread.join()
      self._log_to_cloudwatch(["POSITRON_SIGNAL_EOS"])

  def _log_to_cloudwatch(self, messages: list, level = INFO):
    timestamp = int(round(time.time() * 1000))
    log_events = [{
        'timestamp': timestamp,
        'message': json.dumps({'timestamp': timestamp, 'log_level': logging.getLevelName(level), 'message': message, 'app_name': 'remote_machine'})
    } for message in messages]
    log_stream_name = f'positron-job-{runner_env.JOB_ID}'
    # print(f'log_stream_name: {log_stream_name}')
    log_group_name = runner_env.AWS_JOB_LOG_GROUP_NAME
    # print(f'log_group_name: {log_group_name}')

    # print(f'log_events: {log_events}')
    
    try:
        self.__cloudwatch_client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=log_events
        )
    except Exception as e:
        print(f'Failed to submit logs: {e}')

  def _start_error_batch_thread(self):
    self._stop_event = threading.Event()
    self._batch_thread = threading.Thread(target=self._batch_errors_to_cloudwatch)
    self._batch_thread.daemon = True
    self._batch_thread.start()

  def _batch_errors_to_cloudwatch(self):
    while not self._stop_event.is_set():
        time.sleep(2)  # Batch every 2 seconds
        if self.stderr:
            batched_errors = self.stderr[:]
            self.stderr.clear()
            self._log_to_cloudwatch(batched_errors, ERROR)

logger = CloudLogger()
