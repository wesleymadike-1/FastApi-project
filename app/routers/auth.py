from fastapi import FastAPI, Depends, HTTPException, status,APIRouter
from sqlalchemy.orm import Session
from app.database import get_db

from app.db_models import User
from app import Pass_Hash_Algo ,token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

'''
#login steps:
- the OAuth2PasswordRequestForm have keys of username and password
- Check if user with given email exists.
- If the user exists, verify the provided password against the stored hashed password by hashing the provided password and comparing it to the stored hash.
-if the password matches, authentication is successful:
    -create a token and return it to the user
    -verify the token signature on subsequent requests to protected routes
    -expire the token after a certain period for security
'''

@router.post("/")
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #verify user exists
    db_user = db.query(User).filter(User.email == credentials.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="incorrect credentials")

    if not Pass_Hash_Algo.verify_password(credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    
    #create token
    access_token = token.create_access_token(data={"sub": db_user.id})

    #
    return {"access_token": access_token, "token_type": "bearer"}