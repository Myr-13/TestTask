from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from time import time
from sqlalchemy.orm import Session
from jose import jwt

from src.models.models import User
import src.base.config as config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(pw: str) -> str:
	return pwd_context.hash(pw)


def verify_password(pw: str, hash_pw: str) -> bool:
	return pwd_context.verify(pw, hash_pw)


def decode_token(token: str) -> dict:
	return jwt.decode(token, config.CONFIG["jwt_secret"])


async def login(*, email: str, password: str, db: Session) -> str:
	stmt: User | None = db.query(User).filter(User.email == email).first()
	if not stmt or not verify_password(password, stmt.password_hash):
		raise ValueError("Invalid email or password")

	return jwt.encode(
		{"usr_id": stmt.id, "exp": datetime.now(UTC) + timedelta(seconds=30), "iat": datetime.now(UTC)},
		config.CONFIG["jwt_secret"]
	)


async def register(*, email: str, password: str, db: Session) -> None:
	db_user = db.query(User).filter(User.email == email).first()
	if db_user:
		raise ValueError("Email already registered")

	db_user = User(
		email=email,
		password_hash=get_password_hash(password)
	)
	db.add(db_user)
	db.commit()
