from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.errors.exceptions import BadRequestException, NotFoundException
from src.config.settings import settings


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundException)
    async def handle_not_found(_: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=404,
            content={
                "error": "Not Found",
                "message": exc.message,
            },
        )

    @app.exception_handler(BadRequestException)
    async def handle_bad_request(_: Request, exc: BadRequestException):
        return JSONResponse(
            status_code=400,
            content={
                "error": "Bad Request",
                "message": exc.message,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(_: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation Error",
                "message": "Request validation failed",
                "details": exc.errors(),
            },
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, exc: Exception):
        details = str(exc) if settings.APP_ENV == "development" else "Contact support"
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred",
                "details": details,
            },
        )
