from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional

class UserCreate(BaseModel):
    username :str
    full_name: str
    email: EmailStr
    # the password is required and cant be omitted (...) min_length is 9 characters.
    hashed_password: str = Field(..., min_length=9)
    
class UserResponse(BaseModel):
    username: str
    full_name: str
    email: EmailStr

    class Config:
        orm_mode = True

