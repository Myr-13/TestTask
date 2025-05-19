import sqlalchemy

from src.models.user import User
from src.models.book import Book, BorrowedBook


def create_database(database_path: str):
	engine = sqlalchemy.create_engine(f"sqlite:///./{database_path}")
	User.metadata.create_all(engine)
	Book.metadata.create_all(engine)
	BorrowedBook.metadata.create_all(engine)
