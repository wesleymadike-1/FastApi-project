from fastapi import FastAPI, Depends, HTTPException, status,APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate ,UserResponse
from app.db_models import User
from app import Pass_Hash_Algo

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED ,response_model=UserResponse)
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



@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.get("/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return list(users)


@router.put("/{user_id}", response_model=UserResponse)
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



@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(db_user)
    db.commit()
    return None