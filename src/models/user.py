from sqlalchemy import Column, Integer, String

from src.models.base import Base


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	email = Column(String, nullable=False)
	password_hash = Column(String, nullable=False)
