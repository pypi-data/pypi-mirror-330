from dataclasses import dataclass, asdict
from common.exceptions import DeserializationException
from typing import Union
import json
import sys

# this function is used exclusively in the MetaData class
def get_python_version():
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

@dataclass
class FunctionHashes:
    func_hash: Union[None, str] = None
    args_hash: Union[None, str] = None
    kwargs_hash: Union[None, str] = None
    result_hash: Union[None, str] = None
    exception_hash: Union[None, str] = None

# TODO: should we convert to a yaml format and stringify/parse the same as JobConfig?
@dataclass
class MetaData:
    """Metadata about the serialized data or functions."""

    sha256_hash: FunctionHashes
    version: str = "2023-04-24"
    python_version: str = get_python_version()
    serialization_module: str = "cloudpickle"

    def to_json(self):
        return json.dumps(asdict(self)).encode()

    @staticmethod
    def from_json(s):
        try:
            obj = json.loads(s)
        except json.decoder.JSONDecodeError:
            raise DeserializationException("Corrupt metadata file. It is not a valid json file.")

        sha256_hash = obj.get("sha256_hash")
        metadata = MetaData(sha256_hash=sha256_hash)
        metadata.version = obj.get("version")
        metadata.python_version = obj.get("python_version")
        metadata.serialization_module = obj.get("serialization_module")

        if not sha256_hash:
            raise DeserializationException(
                "Corrupt metadata file. SHA256 hash for the serialized data does not exist. "
                "Please make sure to install SageMaker SDK version >= 2.156.0 on the client side "
                "and try again."
            )

        if not (
            metadata.version == "2023-04-24" and metadata.serialization_module == "cloudpickle"
        ):
            raise DeserializationException(
                f"Corrupt metadata file. Serialization approach {s} is not supported."
            )

        return metadata