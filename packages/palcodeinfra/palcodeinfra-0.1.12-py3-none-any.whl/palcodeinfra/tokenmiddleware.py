from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

class TokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth = request.headers.get("Authorization")
        if not auth:
            return JSONResponse(status_code=400, content={"detail": "Missing Authorization header"})        
        request.state.token = auth
        response = await call_next(request)
        return response
    

    # add middleware to support dynamic log level update
    #Business specific error codes