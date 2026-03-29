from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class ServiceError(Exception):
    def __init__(self, message: str, status_code: int, service_name: str):
        self.message = message
        self.status_code = status_code
        self.service_name = service_name
        super().__init__(self.message)


def http_exception_handler(_: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "HTTP Error", "message": str(exc.detail)},
    )


def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Request validation failed",
            "details": exc.errors(),
        },
    )


def service_error_handler(_: Request, exc: ServiceError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Service Error",
            "message": exc.message,
            "service": exc.service_name,
        },
    )


def general_exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "details": str(exc),
        },
    )
