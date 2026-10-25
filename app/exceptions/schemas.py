from enum import Enum

from pydantic import BaseModel

class ErrorType(str, Enum):
    BAD_REQUEST = "BAD_REQUEST"
    NOT_FOUND = "NOT_FOUND"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"

class DetailType(str, Enum):
    NOT_FOUND = "NOT_FOUND"

class BaseErrorModel(BaseModel):
    type: ErrorType
    description: str

class DetailModel(BaseModel):
    name: str
    error: DetailType

class ValidationErrorModel(BaseErrorModel):
    details: list[DetailModel]