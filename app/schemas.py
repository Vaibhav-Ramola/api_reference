from datetime import datetime
from os import access
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
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

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode=True

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut          # as a result of setting up relationship UserOut object as pydantic model can be returned

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserLogin(BaseModel):
    password: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode=True

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dif: conint(le=1)