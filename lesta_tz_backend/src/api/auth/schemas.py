from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    pwc_code: int

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: Annotated[str, StringConstraints(min_length=6)]


class LoginRequestBody(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=6)]
    pwc_code: int


class Token(BaseModel):
    access_token: str
    refresh_token: str

class PwcCodeRequestBody(BaseModel):
    email: EmailStr

class PwcCodeResponse(BaseModel):
    email: EmailStr
    pwc_code: str