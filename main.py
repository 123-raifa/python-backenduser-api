from fastapi import FastAPI

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


