from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.errors.exceptions import NotFoundException, ValidationException, BadRequestException, ConflictException
from src.config.settings import settings


def _serialize_error_details(errors: list) -> list:
    """Convert validation errors to JSON-serializable format.
    
    Removes non-serializable objects like exception instances and extracts
    relevant error information.
    """
    serialized = []
    for error in errors:
        serialized_error = {
            "field": ".".join(str(loc) for loc in error.get("loc", [])),
            "message": error.get("msg", "Validation error"),
            "input": error.get("input"),
            "type": error.get("type", "unknown"),
        }
        serialized.append(serialized_error)
    return serialized


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundException)
    async def handle_not_found(_: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "Not Found",
                "message": exc.message,
                "status": "error",
            },
        )

    @app.exception_handler(ValidationException)
    async def handle_validation_exception(_: Request, exc: ValidationException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Validation Error",
                "message": exc.message,
                "status": "error",
            },
        )

    @app.exception_handler(BadRequestException)
    async def handle_bad_request(_: Request, exc: BadRequestException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Bad Request",
                "message": exc.message,
                "status": "error",
            },
        )

    @app.exception_handler(ConflictException)
    async def handle_conflict(_: Request, exc: ConflictException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "Conflict",
                "message": exc.message,
                "status": "error",
            },
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(_: Request, exc: RequestValidationError):
        """Handle Pydantic validation errors with serializable error details."""
        serialized_errors = _serialize_error_details(exc.errors())
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation Error",
                "message": "Request validation failed",
                "details": serialized_errors,
                "status": "error",
            },
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, exc: Exception):
        details = str(exc) if settings.APP_ENV == "development" else "Contact support"
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred",
                "details": details,
                "status": "error",
            },
        )
