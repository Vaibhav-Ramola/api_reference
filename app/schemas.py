from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
# from typing import Optional

# This is the Schema
class PostBase(BaseModel):              # will check if the post request has all these fields or not if not will through error automatucally
    title: str
    content: str
    published: bool = True            # default value set to True
    # rating: Optional[int] = None      # a completely optional field of type int, defaults to a value of none

class PostCreat(PostBase):
    pass

# Schema for the response we obtain from the database
# used to define what all information we need in the response
class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    id: int
    password: str
    email: EmailStr

class TokenData(BaseModel):
    id: Optional[str] = None
