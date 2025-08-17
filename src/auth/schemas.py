from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class BaseUserModel(BaseModel):
    email: EmailStr = Field(max_length=40)

    class Config:
        orm_mode = True


class UserCreateModel(BaseUserModel):
    first_name: Optional[str] = Field(default=None, max_length=15)
    last_name: Optional[str] = Field(default=None, max_length=15)
    username: Optional[str] = Field(default=None, max_length=10)
    password: str = Field(min_length=6, max_length=128)


class UserLoginModel(BaseUserModel):
    password: str = Field(min_length=6, max_length=128)
