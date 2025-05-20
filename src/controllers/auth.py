import jose
from sqlalchemy import select

from src.base.database import DATABASE
from src.models.user import User


def login(*, email: str, password: str) -> str | None:
	stmt = select(User).where(User.email == email)

	print(DATABASE.engine)
	for user in DATABASE.session.scalars(stmt):
		print(user)


def register(*, email: str, password: str) -> str | None:
	pass
