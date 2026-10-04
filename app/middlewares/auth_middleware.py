from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from jose import jwt

SECRETE_KEY = "thisIsTheSecreteKey"
ALGO= "HS256"
def auth_middleware(app:FastAPI):
    @app.middleware("http")
    async def verify_token(request:Request, call_next):
        public_routes = ["/auth/login", "/auth/signup", "/docs", "/openapi.json"]

        if request.url.path in public_routes:
            return await call_next(request)

        auth_header=   request.headers.get("Authorization")
    
        if not auth_header:
            return JSONResponse(
                status_code= 401,
                content={"details":"Authorization failed"}
            )
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(
                token,
                SECRETE_KEY,
                ALGO
            )
        
            user_id = payload.get("sub")
            if not user_id:
                return JSONResponse(
                    status_code=401,
                    content={"details":"Invalid token"}
                )
            request.state.user_id = user_id
        except:
            return JSONResponse(
                status_code=401,
                content={"message":"Invalid or expired token"}
            )
        response = await call_next(request)
        return response