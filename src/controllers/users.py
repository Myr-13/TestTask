from sqlalchemy.orm import Session
from jose import JWTError, ExpiredSignatureError
from datetime import datetime

from src.models.models import Book, BorrowedBook
from src.models.schemas import BorrowedBookObject
from src.controllers.auth import decode_token


async def get_books_list(*, token: str, db: Session) -> list[BorrowedBook]:
	# Check auth token
	try:
		token_data = decode_token(token)
		user_id = int(token_data["sub"])
	except ExpiredSignatureError:
		raise ValueError("Token is expired")
	except JWTError:
		raise ValueError("Invalid token")

	books_set = db.query(BorrowedBook).filter(BorrowedBook.user_id == user_id, BorrowedBook.return_date == None)
	out = []

	for book in books_set:
		book: BorrowedBook

		out.append(BorrowedBookObject(
			id=book.id,
			book_id=book.book_id,
			borrow_date=datetime.fromtimestamp(book.borrow_date)
		))

	return out
