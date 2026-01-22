import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_models import User
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#algorithm is like the type of pot we use to cook the token
ALGORITHM = settings.ALGORITHM
#this is your unique signature you use to sign documents, it should be kept secret!!!
# use openssl rand -hex 32 or 64 to generate a strong secret key
SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    # the header and payload are base64 encoded (like being hashed) before the key is added
    # signature = header + payload + secret_key using algorithm
    # token = header + payload + signature

def create_access_token(data: dict, expires_delta: timedelta | None = None)-> str:
    payload = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    payload.update({"exp": expire})
    Token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return Token


def verify_access_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> int:
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
    
    UserData= db.query(User).filter(User.id == userid).first()
    if UserData is None:
        raise credentials_exception
    
    return UserData