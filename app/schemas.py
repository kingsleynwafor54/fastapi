from typing import Optional
from datetime import datetime
from pydantic import BaseModel,EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

class Post(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 (use orm_mode=True for v1)


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


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]