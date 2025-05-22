import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.models.models import Book
from src.models.schemas import BookObject


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
