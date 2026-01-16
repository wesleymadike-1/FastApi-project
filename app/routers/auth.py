from fastapi import FastAPI, Depends, HTTPException, status,APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Login
from app.db_models import User
from app import Pass_Hash_Algo

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

'''
#login steps:
- Check if user with given email exists.
- If the user exists, verify the provided password against the stored hashed password by hashing the provided password and comparing it to the stored hash.
-if the password matches, authentication is successful:
    -create a token and return it to the user
    -verify the token signature on subsequent requests to protected routes
    -expire the token after a certain period for security
'''

@router.post("/")
def login(credentials: Login, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == credentials.email).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="incorrect credentials")

    if not Pass_Hash_Algo.verify_password(credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    
    
    
    return {"message": "Login successful"}