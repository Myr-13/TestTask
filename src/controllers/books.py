import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select
from jose import JWTError, ExpiredSignatureError

from src.models.models import Book
from src.models.schemas import BookObject
from src.controllers.auth import decode_token


async def get(*, db: Session) -> list[BookObject]:
	stmt = select(Book)
	books = []

	for book in db.scalars(stmt):
		d = datetime.datetime.fromordinal(book.release_date)
		print(d, book.isbn)

		books.append(BookObject(
			id=book.id,
			name=book.name,
			author=book.author,
			release_date=d,
			isbn=book.isbn,
			count=book.count
		))

	return books


async def borrow(*, token: str, book_id: int, db: Session) -> list[BookObject]:
	try:
		token_data = decode_token(token)
	except ExpiredSignatureError:
		raise ValueError("Token is expired")
	except JWTError as e:
		raise ValueError("Invalid token")

	stmt = select(Book)
	books = []

	for book in db.scalars(stmt):
		d = datetime.datetime.fromordinal(book.release_date)

		books.append(BookObject(
			id=book.id,
			name=book.name,
			author=book.author,
			release_date=d,
			isbn=book.isbn,
			count=book.count
		))

	return books
