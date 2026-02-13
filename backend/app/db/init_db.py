from sqlmodel import SQLModel
from app.db.session import engine
from app.models.user import *

def init_db():
    SQLModel.metadata.create_all(engine)