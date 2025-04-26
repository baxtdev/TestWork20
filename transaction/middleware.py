from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, api_key: str):
        super().__init__(app)
        self.api_key = api_key

    async def dispatch(self, request: Request, call_next):
        api_key_header = request.headers.get("Authorization")
        
        if api_key_header is None or not api_key_header.startswith("ApiKey "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing"}
            )

        api_key = api_key_header.split(" ")[1]
        if api_key != self.api_key:
            return JSONResponse(
                status_code=403,
                content={"detail": "Invalid API key"}
            )

        response = await call_next(request)
        return response
