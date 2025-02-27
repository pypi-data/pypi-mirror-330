import subprocess
import threading
import select
import os
from typing import Dict


def run_local_docker_container(job_id: str, base_path: str):
    print("run_local_docker_container")
    
    # env = {}
    env: Dict[str, str] = {}
    env['JOB_ID'] = job_id
    if os.getenv('REMOTE_FUNCTION_SECRET_KEY'):
        env['REMOTE_FUNCTION_SECRET_KEY'] = os.getenv('REMOTE_FUNCTION_SECRET_KEY')
    print("env=", env)

    p = subprocess.Popen(
        "env && /usr/local/bin/docker compose up --no-color --build --force-recreate",
        text=True,
        shell=True,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        env=env,
        cwd=f"{base_path}/test/job_runner",
    )
    log_stop_event = threading.Event()
    stdout_thread = threading.Thread(target=logging_thread, args=(p.stdout, "stdout", log_stop_event)); stdout_thread.start()
    stderr_thread = threading.Thread(target=logging_thread, args=(p.stderr, "stderr", log_stop_event)); stderr_thread.start()
    p.wait()
    log_stop_event.set()
    stdout_thread.join()
    stderr_thread.join()
    print("p.returncode=", p.returncode)

def logging_thread(pipe, stream_name: str, stop_event: threading.Event):
    try:
        with pipe:
            while not stop_event.is_set():
                # Calling pipe.readline() will hang the process until a new line is available
                # however, if no new lines are available, we want to check if the thread should stop
                ready, _, _ = select.select([pipe], [], [], 0.1)
                if ready:
                    # TODO: Can I iterate over the pipe and process everything that's ready?
                    line = pipe.readline()
                    if not line:
                        break
                    if line.strip():
                        if stream_name == "stdout":
                            print(line.rstrip())
                        else:
                            print("ERROR: " + line.rstrip())
                else:
                    stop_event.wait(1)

            # Read one last time.
            ready, _, _ = select.select([pipe], [], [], 0.1)
            if ready:
                for line in pipe:
                    if line.strip():
                        if stream_name == "stdout":
                            print(line.rstrip())
                        else:
                            print("ERROR: " + line.rstrip())
            # TODO: Do we need to check one more time for outstanding data in the pipe?
            # logger.debug(f'Logging thread for: {stream_name} stopped')
    except Exception as e:
        print(f'Logging thread for: {stream_name} stopped with exception: {e}')




