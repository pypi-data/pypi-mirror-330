from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import uuid

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        request_id = request.headers.get('X-Request-ID', None)
        
        if not request_id:
            request_id = uuid.uuid4()
            request.state.request_id = request_id

        response = await call_next(request)           
        response.headers.append("X-Request-ID", str(request_id))    
        return response