from sqlalchemy import Column, Integer, String, BigInteger
from enum import Enum

from src.base.database import Base


class Rights(Enum):
	foo = 1


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	email = Column(String, nullable=False)
	password_hash = Column(String, nullable=False)
	rights = Column(Integer, nullable=False, default=0)


class Book(Base):
	__tablename__ = "books"

	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String, nullable=False)
	author = Column(String, nullable=False)
	release_date = Column(Integer, nullable=False)
	isbn = Column(BigInteger, default=None)
	count = Column(Integer, nullable=False, default=1)


class BorrowedBook(Base):
	__tablename__ = "borrowed_books"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, nullable=False)
	book_id = Column(Integer, nullable=False)
	borrow_date = Column(Integer, nullable=False)
	return_date = Column(Integer, default=None)
