from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate ,UserResponse
from app.db_models import User
from app import Pass_Hash_Algo
from typing import List


description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items 

You can **read items**.

## Users

You will be able to:
kk
* **Create users**.
* **Read users**.
"""

app = FastAPI(
    title="WESLEY MADIKE API",
    description=description,
)

@app.post("/users", status_code=status.HTTP_201_CREATED ,response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    user.hashed_password = Pass_Hash_Algo.get_password_hash(user.hashed_password)
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return list(users)

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db_user.username = user.username
    db_user.email = user.email
    db_user.full_name = user.full_name

    user.hashed_password = Pass_Hash_Algo.get_password_hash(user.hashed_password)
    db_user.hashed_password = user.hashed_password  # In a real app, hash the password!
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(db_user)
    db.commit()
    return None