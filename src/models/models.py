from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, BigInteger, DateTime
import sqlalchemy.types as types

from src.base.database import Base


class MyEpochType(types.TypeDecorator):
	impl = types.Integer
	cache_ok = True

	epoch = datetime(1970, 1, 1)

	def process_bind_param(self, value, dialect):
		return (value - self.epoch).days

	def process_result_value(self, value, dialect):
		return self.epoch + timedelta(days=value)


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	email = Column(String, nullable=False)
	password_hash = Column(String, nullable=False)


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
	borrow_date = Column(MyEpochType, nullable=False)
	return_date = Column(MyEpochType, default=None)
