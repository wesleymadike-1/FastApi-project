from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import UserCreate, UserResponse
from .database import get_db
from .db_models import User
from typing import List
from passlib.context import CryptContext

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users**.
* **Read users**.
"""

app = FastAPI(
    title="WESLEY MADIKE API",
    description=description,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
   
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



@app.get("/")
def root():
    return {"message": "HellHHnbkhjguiyfvo Wnc000"}