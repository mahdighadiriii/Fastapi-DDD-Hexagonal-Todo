from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"Request: {request.method} {request.url}")

        response = await call_next(request)

        print(f"Response status: {response.status_code}")

        return response
