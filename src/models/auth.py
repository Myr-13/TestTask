from typing import Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
	email: str
	password: str


class LoginResponse(BaseModel):
	code: int
	auth_token: Optional[str] = None
	message: Optional[str] = None


class RegisterRequest(BaseModel):
	email: str
	password: str


class RegisterResponse(BaseModel):
	code: int
	message: str
