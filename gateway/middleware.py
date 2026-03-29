import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        # Minimal structured log for gateway request tracing.
        print(
            f"[{request.method}] {request.url.path} -> {response.status_code} "
            f"({duration_ms:.2f} ms)"
        )
        return response
