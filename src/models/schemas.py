import datetime
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


class BookObject(BaseModel):
	id: int
	name: str
	author: str
	release_date: datetime.datetime
	isbn: Optional[int]
	count: int


class BooksResponse(BaseModel):
	books: list[BookObject]


class BookBorrowRequest(BaseModel):
	book_id: int


class BookReturnRequest(BaseModel):
	book_id: int


class BorrowedBookObject(BaseModel):
	id: int
	book_id: int
	borrow_date: datetime.datetime
