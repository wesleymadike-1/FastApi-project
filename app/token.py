import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_models import User





#algorithm is like the type of pot we use to cook the token
ALGORITHM = "HS256"
#this is your unique signature you use to sign documents, it should be kept secret!!!
SECRET_KEY = "your_secret_key_here"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
    # the header and payload are base64 encoded (like being hashed) before the key is added
    # signature = header + payload + secret_key using algorithm
    # token = header + payload + signature

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    payload = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    payload.update({"exp": expire})
    Token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return Token


def verify_access_token(token: str , db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userid : int = payload.get("sub")
        if userid is None:
            raise credentials_exception
        
    except InvalidTokenError:
        raise credentials_exception
    
    UserId = db.query(User).filter(User.id == userid).first()
    if UserId is None:
        raise credentials_exception
    
    return UserId