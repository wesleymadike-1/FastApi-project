from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    

# Response model for user creation
class UserResponse(BaseModel):
    id: int
    username: str
   

    class Config:
        orm_mode = True