from fastapi import FastAPI, Depends, HTTPException
from app.database import engine
from app.models import Base
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.schemas import UserUpdate

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

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # 1️⃣ check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # 2️⃣ create new user
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}

@app.patch("/users/{user_id}")
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.id == user_id).first()

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.name is not None:
        existing_user.name = user.name

    if user.email is not None:
        existing_user.email = user.email

    db.commit()
    db.refresh(existing_user)

    return existing_user

