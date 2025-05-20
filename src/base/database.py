import sqlalchemy
from sqlalchemy.orm import Session

from src.models.user import User
from src.models.book import Book, BorrowedBook


class Database:
	def __init__(self):
		self.engine: sqlalchemy.Engine = ...
		self.session: Session = ...

	def create(self, database_path: str):
		self.engine = sqlalchemy.create_engine(f"sqlite:///./{database_path}")
		User.metadata.create_all(self.engine)
		Book.metadata.create_all(self.engine)
		BorrowedBook.metadata.create_all(self.engine)

		self.session = Session(bind=self.engine)


DATABASE: Database = Database()
