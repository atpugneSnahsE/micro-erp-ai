from pydantic import (
    BaseModel,
    EmailStr
)


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "staff"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str