from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.init_db import init_db
from app.api.v1.endpoints import auth, projects
from app.core.logger import setup_logging
from app.core.config import settings
from app.api.v1.endpoints import users

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    init_db()
    yield

app = FastAPI(
    title="TaskFlow API",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(projects.router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])

@app.get("/")
def root():
    return {"message": "Hello TaskFlow! App is running"}