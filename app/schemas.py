from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Annotated




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
        from_attributes = True

class PostCreate(BaseModel):
    title: str
    content: str
    
class PostResponse(BaseModel):
    id: int
    owner_id: int
    title: str
    content: str
    owner: UserResponse

    class Config:
        from_attributes = True

class Like(BaseModel):
    post_id: int
    # dir ensures the direction is either 0 or 1
    dir: Annotated[int,Field(ge=0, le=1)]
