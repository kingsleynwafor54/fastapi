from typing import Literal, Optional
from datetime import datetime
from pydantic import BaseModel,EmailStr
from pydantic.types import conint

class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]

class UserCreate(BaseModel):
    email:EmailStr
    password:str


class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime
    # class Config: 
    #     orm_mode=True
    class Config:
        from_attributes = True  # Pydantic v2 (use orm_mode=True for v1)

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

class Post(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id:int
    owner:UserOut

    class Config:
        from_attributes = True  # Pydantic v2 (use orm_mode=True for v1)



class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]

