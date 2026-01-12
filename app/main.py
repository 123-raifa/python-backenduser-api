from app.database import engine
from fastapi import FastAPI
from app.database import engine
from app.models import Base

app = FastAPI()

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

