import dill
import platform
import pathlib

do_not_load = ['open', 'os', 'do_not_load', 'remote_load_pickle', 'remote_local_pickle']

LOCAL_PICKLE = 'cell.pkl'
REMOTE_PICKLE = 'cell_result.pkl'

plt = platform.system()
if plt == 'Linux': pathlib.WindowsPath = pathlib.PosixPath

def remote_load_pickle():
    file = open(LOCAL_PICKLE, 'rb')
    unpickler = dill.Unpickler(file)
    user_ns = unpickler.load()
    file.close()
    if user_ns is not None:
        for key, value in user_ns.items():
            if key not in do_not_load and (key not in globals() or not callable(globals()[key])):
                globals()[key] = value

def remote_local_pickle(user_ns: dict):
    ns_copy = user_ns.copy()
    # baditems = dill.detect.baditems(user_ns)
    # for baditem in baditems:
    ns_copy = {key: value for key, value in ns_copy.items() if key not in do_not_load}
    
    file = open(REMOTE_PICKLE, 'wb')
    protocol = dill.settings['protocol']
    pickler = dill.Pickler(file, protocol)
    pickler._byref = False   # disable pickling by name reference
    pickler._recurse = False # disable pickling recursion for globals
    pickler._session = True  # is best indicator of when pickling a session
    pickler._first_pass = True
    pickler.dump(ns_copy)
    file.flush()
    file.close()

remote_load_pickle()
    
### {cell}

remote_local_pickle(globals())