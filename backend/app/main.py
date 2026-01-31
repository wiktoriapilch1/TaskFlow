from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.init_db import init_db
from app.api.v1.endpoints import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="TaskFlow API",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("/")
def root():
    return {"message": "Hello TaskFlow! App is running"}