from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="TaskFlow API",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/")
def root():
    return {"message": "Hello TaskFlow! App is running"}