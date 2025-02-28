from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        #response.headers.append("X-Correlation-ID",request.headers.get("X-Correlation-ID"))
        print(f"Response: {response.status_code}")
        return response