from fastapi import FastAPI, Request, HTTPException, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from starlette.routing import Match
from palcodeinfra.database import Database
from sqlalchemy import text
from dotenv import load_dotenv
import os

class UserIdMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, excluded_paths):
        super().__init__(app)
        self.excluded_paths = excluded_paths

    async def IsUserIdValid(self, user_id):   
        load_dotenv() 

        database_url = os.environ.get("IDENTITY_DATABASE_URL")
        if not database_url:
            raise ValueError("IDENTITY_DATABASE_URL is not set in the .env file")
                    
        db_object = Database(database_url)
        db_engine = db_object.get_engine()
        with db_engine.connect() as connection:
            query = text("SELECT 1 FROM identity.user WHERE user_id = :user_id LIMIT 1")
            result = connection.execute(query, {"user_id": user_id})
            rows = result.fetchone()
            return rows is not None

    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)
        
        user_id = request.headers.get("X-User-ID")
        
        if not user_id:
            return JSONResponse(status_code=400, content={"detail": "Missing X-User-ID header"})
        
        result = await self.IsUserIdValid(user_id)
        if not result:
            return JSONResponse(status_code=403, content={"detail": "Invalid X-User-ID header value"})
        
        request.state.user_id = user_id
        response = await call_next(request)
        return response