import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone

#algorithm is like the color of the pen we use to sign. e.g Red pen
ALGORITHM = "HS256"
#this is your unique signature you use to sign documents, it should be kept secret!!!
SECRET_KEY = "your_secret_key_here"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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


# def verify_access_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except InvalidTokenError:
#         return None