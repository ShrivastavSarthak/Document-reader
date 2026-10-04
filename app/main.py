from fastapi import FastAPI
from app.routes.documents import document_route
from app.routes.auth_route import auth_route 
from app.db.db import engine, Base
from app.middlewares.auth_middleware import auth_middleware

app = FastAPI(
    title="Mini Rag Doc chat",
    version= "1.0.0"
)
auth_middleware(app)
print(Base.metadata.tables.keys())
Base.metadata.create_all(bind=engine)

app.include_router(document_route)
app.include_router(auth_route)

@app.get("/")
async def root():
    return {
        "message":"Mini RAG API is running"
    }