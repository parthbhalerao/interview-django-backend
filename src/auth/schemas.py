from ninja import Schema
from pydantic import EmailStr
from typing import Optional

class UserSchema(Schema):
    id: int
    username: str
    email: str
    is_active: bool
    first_name: str | None = None
    last_name: str | None = None

class LoginSchema(Schema):
    username: str
    password: str

class RegisterSchema(Schema):
    username: str
    email: EmailStr
    password: str

class TokenResponseSchema(Schema):
    access: str
    refresh: str

class PasswordResetRequestSchema(Schema):
    email: str

class PasswordResetConfirmSchema(Schema):
    token: str
    password: str

class TokenRefreshSchema(Schema):
    refresh: str 