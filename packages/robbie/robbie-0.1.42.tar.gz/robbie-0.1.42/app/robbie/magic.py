import platform
import pathlib
import os
import threading
import select
import dill
import subprocess
import shutil
from IPython.core.magic import (Magics, magics_class, cell_magic)
from importlib.resources import files
from robbie.requirements_detection.main import show

plt = platform.system()
if plt == 'Windows': pathlib.PosixPath = pathlib.WindowsPath

LOCAL_PICKLE = 'cell.pkl'
REMOTE_PICKLE = 'cell_result.pkl'
REQUIREMENTS_FILENAME = 'cell_requirements.txt'
CELL_EXECUTABLE_FILENAME = 'cell_output.py'
JOB_RESULTS = 'job-execution'

do_not_load = ['open', 'os', 'do_not_load', 'load_pickle', 'local_pickle']

def local_pickle(user_ns: dict):
    ns_copy = user_ns.copy()
    baditems = dill.detect.baditems(user_ns)
    for baditem in baditems:
        ns_copy = {key: value for key, value in ns_copy.items() if value != baditem and key not in do_not_load}
    
    file = open(LOCAL_PICKLE, 'wb')
    protocol = dill.settings['protocol']
    pickler = dill.Pickler(file, protocol)
    pickler._byref = False   # disable pickling by name reference
    pickler._recurse = False # disable pickling recursion for globals
    pickler._session = True  # is best indicator of when pickling a session
    pickler._first_pass = True
    pickler.dump(ns_copy)
    file.flush()
    file.close()

def load_pickle(filename):
    file = open(filename, 'rb')
    unpickler = dill.Unpickler(file)
    user_ns = unpickler.load()
    file.close()
    return user_ns

# Registers this class name as a magic definition with ipython.
# Run with %%robbie
@magics_class
class robbie_magic(Magics):
    def write_requirements(self, filename: str):
        show(html=False, write_req_file=True, req_file_name=filename, caller_globals=self.shell.user_ns)
        
    
    @cell_magic
    def robbie(self, _, cell):

        # Ensure dill is installed and save the current session to a pickle file
        local_pickle(self.shell.user_ns)

        # get deps and ensure we'll install them.
        self.write_requirements(REQUIREMENTS_FILENAME)


        # create a file that wraps the cell and loads the pickle file
        exec_wrap_file = files('robbie').joinpath('executable_wrapper.py')
        exec_wrap_contents = exec_wrap_file.read_text().strip()
        exec_text = exec_wrap_contents.replace('### {cell}', cell)
        with open(CELL_EXECUTABLE_FILENAME, 'w') as f:
            f.write(exec_text)
        
        # Create a job on the fly and run the cell file in robbie
        if platform.system() == 'Windows':
            rc = monitor_win_process()
        else:
            rc = monitor_nix_process()

        # If the job was successful, load the results back into the ipython environment
        if rc == 0:
            # Job results should come back as a pkl file. We load the results back into the ipython environment
            try:
                copy_ns = load_pickle(f'{REMOTE_PICKLE}')
                for key, value in copy_ns.items():
                    self.shell.user_ns[key] = value
            except Exception as e:
                print(f'Error loading results: {e}')
                pass
        else:
            print(f'Error robbie run: {rc}')

        # Clean up env
        rm(CELL_EXECUTABLE_FILENAME)
        rm(LOCAL_PICKLE)
        rm(REMOTE_PICKLE)
        rm(REQUIREMENTS_FILENAME)
        rmdir(JOB_RESULTS)


def remove_line(multiline_str, match) -> str:
    lines = multiline_str.splitlines()  # Split into lines
    filtered_lines = [line for line in lines if match not in line]  # Filter lines
    return "\n".join(filtered_lines)  # Join the remaining lines

def rmdir(dirname):
    try:
        shutil.rmtree(dirname)
    except FileNotFoundError:
        pass

def rm(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass

def monitor_win_process() -> int:
    print("Monitoring process in Windows")
    os.environ["PYTHONIOENCODING"] = "utf-8"
    command = f'robbie run --download "{REMOTE_PICKLE}" --tail --y "pip install -r {REQUIREMENTS_FILENAME} && pip install dill && python {CELL_EXECUTABLE_FILENAME}"'
    p = subprocess.Popen(
        command,
        # use a job_config.yaml, this was done to use NERC which has much faster startup times.
        # f'robbie run --tail --y',
        text=True,
        shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8'
    )
    try:
        # Read both stdout and stderr line by line
        for line in p.stdout:
            print(line, end="")  # Avoid adding extra newlines
        for line in p.stderr:
            print("ERROR: " + line, end="")
    except UnicodeEncodeError as e:
        print(f"Unicode error encountered: {e}")
    finally:
        p.stdout.close()
        p.stderr.close()
        p.wait()
    return p.returncode

def monitor_nix_process() -> int:
    print('Monitoring process')
    command = f'robbie run --download "{REMOTE_PICKLE}" --tail --y "pip install -r {REQUIREMENTS_FILENAME} && pip install dill && python {CELL_EXECUTABLE_FILENAME}"'
    p = subprocess.Popen(
        command,
        # use a job_config.yaml, this was done to use NERC which has much faster startup times.
        # f'robbie run --tail --y',
        text=True,
        shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    log_stop_event = threading.Event()
    stdout_thread = threading.Thread(target=logging_thread, args=(p.stdout, "stdout", log_stop_event)); stdout_thread.start()
    stderr_thread = threading.Thread(target=logging_thread, args=(p.stderr, "stderr", log_stop_event)); stderr_thread.start()
    p.wait()
    log_stop_event.set()
    stdout_thread.join()
    stderr_thread.join()
    return p.returncode

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


# Loads the magic class into the runtime ipython environment.
# Load with %load_ext robbie.magic
def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    # You can register the class itself without instantiating it.  IPython will
    # call the default constructor on it.
    ipython.register_magics(robbie_magic)
