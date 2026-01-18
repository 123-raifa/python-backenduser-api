from fastapi import FastAPI, Depends, HTTPException
from app.database import engine
from app.models import Base
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.schemas import UserUpdate
from app.routes.users import router as users_router


app = FastAPI()
app.include_router(users_router)


@app.get("/hello")
def say_hello():
    return {"message": "Hello from backend"}
from pydantic import BaseModel

class NameRequest(BaseModel):
    name: str

@app.post("/greet")
def greet_user(data: NameRequest):
    return {"message": f"Hello {data.name}"}

@app.on_event("startup")
def start_db():
    Base.metadata.create_all(bind=engine)



