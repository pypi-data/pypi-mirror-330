import sys
import atexit
import sentry_sdk
import logging
from typing import Any
from functools import wraps
from importlib.resources import files
from sentry_sdk.integrations.logging import LoggingIntegration
from common.user_config import user_config
from common.common_dump import dump_data

# Load build env
build_env_resource = files('common').joinpath('build_env')
build_env = "local"
if (build_env_resource.is_file()):
    try:
        build_env = build_env_resource.read_text().strip()
    except Exception as e:
        pass

# Initialize Sentry
sentry_sdk.init(
    dsn=user_config.sentry_dsn,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    # Set environment so we can tell the difference between local and deployed
    environment=build_env,
    integrations=[LoggingIntegration(
        level=logging.DEBUG,         # Capture all info and above as breadcrumbs
        event_level=logging.ERROR,
    )],
  )

def track_command_usage(command_name) -> Any:
    """Decorator to track usage of commands in Sentry with arguments."""
    def decorator(func: Any) -> Any:
        @wraps(func)
        def wrapper(*args, **kwargs):
            with sentry_sdk.start_transaction(op="command", name=command_name):
                # Capture command usage event with arguments
                sentry_sdk.capture_event({
                    "message": f"Command Run: {command_name}",
                    "level": "info",
                    "tags": {"command": command_name},
                    "extra": {
                        "arguments": args,
                        "keyword_arguments": kwargs
                    }
                })
                # Execute the command function
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    sentry_sdk.capture_exception(e)
                    sentry_sdk.capture_event({
                        "message": f"Dump details from exception",
                        "level": "info",
                        "extra": dump_data(),
                    })
                    print(f"Trace ID: {sentry_sdk.get_current_span().trace_id}")
                    raise e
        return wrapper
    return decorator

def cleanup():
    # flush sentry events to ensure there's no sentry logging to the user
    sentry_sdk.flush()
    
atexit.register(cleanup)
