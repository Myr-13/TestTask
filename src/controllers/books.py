import datetime
import time

from sqlalchemy.orm import Session
from sqlalchemy import select, update
from jose import JWTError, ExpiredSignatureError

from src.models.models import Book, BorrowedBook
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


async def borrow(*, token: str, book_id: int, db: Session) -> None:
	# Check auth token
	# TODO: OPT: Move this to auth controller
	try:
		token_data = decode_token(token)
		user_id = int(token_data["sub"])
	except ExpiredSignatureError:
		raise ValueError("Token is expired")
	except JWTError:
		raise ValueError("Invalid token")

	# Search for book
	book: Book | None = db.query(Book).filter(Book.id == book_id).first()
	if not book:
		raise ValueError("Book didnt found")

	# Count of books must be more than zero
	if book.count < 1:
		raise ValueError("Catalog dont have enough books")

	# Borrow only 3 books in one time
	borrowed_count: int = db.query(BorrowedBook).filter(BorrowedBook.user_id == user_id).count()
	if borrowed_count >= 3:
		raise ValueError("You already borrowed 3 books")

	# 1 book of each id = 1 user
	have_book: int = db.query(BorrowedBook) \
		.filter(BorrowedBook.user_id == user_id, BorrowedBook.book_id == book_id).count()
	print(have_book)
	if have_book != 0:
		raise ValueError("You already borrowed this book")

	book.count -= 1

	borrowed_book = BorrowedBook(
		user_id=user_id,
		book_id=book.id,
		borrow_date=round(time.time())
	)
	db.add(borrowed_book)
	db.commit()


async def return_(*, token: str, book_id: int, db: Session) -> None:
	pass
