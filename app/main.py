from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from app.exceptions.exceptions import ValidationException, NotFoundException, InternalServerErrorException
from app.routers import categories

app = FastAPI()

app.include_router(categories.router)

@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(exc.content),
    )

@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=HTTP_404_NOT_FOUND,
        content=jsonable_encoder(exc.content),
    )

@app.exception_handler(500)
async def internal_server_error_exception_handler(request: Request, exc: InternalServerErrorException):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(exc.content),
    )
