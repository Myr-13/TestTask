from sqlalchemy import Column, Integer, String, DateTime, BigInteger

from src.models.base import Base


class Book(Base):
	__tablename__ = "books"

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	author = Column(String, nullable=False)
	release_date = Column(DateTime, nullable=False)
	isbn = Column(BigInteger, default=None)
	count = Column(Integer, default=1)


class BorrowedBook(Base):
	__tablename__ = "borrowed_books"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, nullable=False)
	book_id = Column(Integer, nullable=False)
	borrow_date = Column(DateTime, nullable=False)
	return_date = Column(DateTime, default=None)
