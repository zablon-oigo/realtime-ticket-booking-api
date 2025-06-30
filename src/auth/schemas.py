from pydantic import BaseModel 
from sqlmodel import Field
from typing import Optional

class UserCreateModel(BaseModel):
    first_name: Optional[str] = Field(default=None, max_length=15)
    last_name: Optional[str] = Field(default=None, max_length=15)
    username: Optional[str] = Field(default=None, max_length=10)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

    class Config:
        orm_mode = True

class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str  = Field(min_length=6)

    class Config:
        orm_mode = True