import hmac
import hashlib
from typing import Any, Tuple
import cloudpickle

from common.exceptions import SerializationException, DeserializationException

class Serializer:
    """Serializer class for serializing and deserializing objects with CloudPickle."""


    @staticmethod
    def serialize(obj: Any) -> Any:
        try:
            bytes_to_upload = cloudpickle.dumps(obj)
            return bytes_to_upload
        except Exception as e:
            raise SerializationException("Object is not serializable") from e

    @staticmethod
    def deserialize(bytes_to_deserialize: bytes) -> Any:
        try:
            return cloudpickle.loads(bytes_to_deserialize)
        except Exception as e:
            raise DeserializationException(
                "Error when deserializing bytes: {}".format(repr(e))
            ) from e

    @staticmethod
    def compute_hash(buffer: bytes, secret_key: str) -> str:
        return hmac.new(secret_key.encode(), msg=buffer, digestmod=hashlib.sha256).hexdigest()
