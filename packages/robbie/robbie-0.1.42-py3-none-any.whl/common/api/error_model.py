from pydantic import BaseModel
from typing import Optional

class ErrorModel(BaseModel):
    code: Optional[str]

class ResponseErrorModel(BaseModel):
    userFriendlyErrorMessage: Optional[str]
    message: str
    error: Optional[ErrorModel]
    stack: Optional[str]
