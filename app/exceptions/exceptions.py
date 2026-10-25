from fastapi.exceptions import RequestValidationError, HTTPException

from app.exceptions.schemas import DetailModel, ValidationErrorModel, ErrorType, BaseErrorModel


class ValidationException(RequestValidationError):
    def __init__(self, details: list[DetailModel]):
        self.content = ValidationErrorModel(
            type=ErrorType.BAD_REQUEST,
            description="The server could not understand the user's request due to syntax errors or incorrect data structure.",
            details=details,
        )

class NotFoundException(Exception):
    def __init__(self):
        self.content = BaseErrorModel(
            type=ErrorType.NOT_FOUND,
            description="The server cannot find the requested resource."
        )

class InternalServerErrorException(Exception):
    def __init__(self):
        self.content = BaseErrorModel(
            type=ErrorType.INTERNAL_SERVER_ERROR,
            description="The server encountered an unexpected condition."
        )
