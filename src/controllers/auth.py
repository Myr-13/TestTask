from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from sqlalchemy.orm import Session
from jose import jwt

from src.models.models import User
import src.base.config as config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(pw: str):
	return pwd_context.hash(pw)


def verify_password(pw: str, hash_pw: str):
	return pwd_context.verify(pw, hash_pw)


def verify_token(token: str):
	data = jwt.decode(token, config.CONFIG["jwt_secret"])
	return data["exp"] > datetime.now(UTC)


async def login(*, email: str, password: str, db: Session) -> str:
	stmt: User | None = db.query(User).filter(User.email == email).first()
	if not stmt or not verify_password(password, stmt.password_hash):
		raise ValueError("Invalid email or password")

	return jwt.encode(
		{"usr": f"{stmt.id}_{stmt.email}", "exp": datetime.now(UTC) + timedelta(minutes=30)},
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
