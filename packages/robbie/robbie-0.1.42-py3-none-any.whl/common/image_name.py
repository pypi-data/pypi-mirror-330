from common.utils import _current_python_version
from common.constants import *
from common.env_defaults import current
from common.logging_config import logger
from common.api.funding_envs_images import *

# used to construct the image name
IMAGE_VERSION = '1.0.0'
BASE_NAME = "robbie"
LINUX_VERSION = "ubuntu22.04"

DEFAULT_PYTORCH_VERSION_GPU = {
    "py3.9": "2.0",
    "py3.10": "2.2",
    "py3.11": "2.4",
    "py3.12": "2.5",
}

DEFAULT_PYTORCH_VERSION_CPU = {
    "py3.9": "1.13",
    "py3.10": "2.2",
    "py3.11": "2.4",
    "py3.12": "2.5",
}

def get_auto_image_name_and_cluster(fs_id: str, env_id: str, py_vers: str):
    """
    Constructs an image name based on the current environment, chosen cluster, and python version
    """
    logger.debug(f"get_auto_image_name_and_cluster(): {fs_id}, {env_id}, {py_vers}")

    gpu_count, cluster_type = get_gpu_count_and_cluster_from_env(fs_id, env_id)

    # if there are GPUs in the environment, use the GPU image
    
    if (gpu_count == "0" or gpu_count == None or gpu_count == ""):
        proc_type = "cpu"
    else:
        proc_type = "gpu"
    logger.debug(f"proc_type: {proc_type}")

    # if running local use dev images
    if current.name == "local":
        env = "dev"
    else:
        env = current.name

    # most of the time this will be None
    if not py_vers:
        py_vers = _current_python_version()

    python_version = f"py{py_vers}"
    logger.debug(f"Python version string: {python_version}")
    if proc_type == "gpu" and not DEFAULT_PYTORCH_VERSION_GPU.get(python_version):
        logger.debug(f"No default PyTorch GPU version found for: {python_version}")
        return None, None
    if proc_type == "cpu" and not DEFAULT_PYTORCH_VERSION_CPU.get(python_version):
        logger.debug(f"No default PyTorch CPU version found for: {python_version}")
        return None, None
    
    torch_version = DEFAULT_PYTORCH_VERSION_GPU.get(python_version) if proc_type == "gpu" else DEFAULT_PYTORCH_VERSION_CPU.get(python_version)
    image_name = f"{BASE_NAME}:{IMAGE_VERSION}-{proc_type}-{python_version}-torch{torch_version}-{LINUX_VERSION}-{env}"
    logger.debug(f"Automatically generated image name: {image_name}")

    if cluster_type == "DOCKER":
        image_name = "robbie:1.0.0-cpu-py3.10-torch2.2-ubuntu-arm22.04-dev"
    return image_name, cluster_type

    
   
def get_gpu_count_and_cluster_from_env(fs_id: str, env_id: str):
    """ Gets the cluster type from the environment """
    envs = list_environments(fs_id)
    if len(envs) == 0:
        return None, None
    for _, val in envs.items():
        if(val.get(ENV_ID) == env_id):
            logger.debug(f"Environment: {val.get(ENV_NAME)}, Id: {val.get(ENV_ID)}, Cluster type: {val.get(ENV_CLUSTER_TYPE)}, GPU count: {val.get(ENV_GPU_NUMBER)}")
            return val.get(ENV_GPU_NUMBER), val.get(ENV_CLUSTER_TYPE)
    return None, None

      