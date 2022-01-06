from pydantic import (
    BaseModel,
    EmailStr
)
from pydantic.fields import Field


class UserBase(BaseModel):
    email: EmailStr


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)


class Token(BaseModel):
    access_token: str
