from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from sqlalchemy.orm import Session
from jose import jwt, JWTError, ExpiredSignatureError

from src.models.models import User
import src.base.config as config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(pw: str) -> str:
	return pwd_context.hash(pw)


def verify_password(pw: str, hash_pw: str) -> bool:
	return pwd_context.verify(pw, hash_pw)


def encode_token(subject):
	return jwt.encode(
		{"sub": str(subject), "exp": datetime.now(UTC) + timedelta(weeks=30), "iat": datetime.now(UTC)},
		config.CONFIG["jwt_secret"]
	)


def decode_token(token: str) -> dict:
	return jwt.decode(token, config.CONFIG["jwt_secret"])


def check_token(token: str) -> int:
	try:
		token_data = decode_token(token)
		return int(token_data["sub"])
	except ExpiredSignatureError:
		raise ValueError("Token is expired")
	except JWTError:
		raise ValueError("Invalid token")


def user_have_role(user: User, right: int) -> bool:
	return user.rights & right != 0


async def login(*, email: str, password: str, db: Session) -> str:
	user: User | None = db.query(User).filter(User.email == email).first()
	if not user or not verify_password(password, user.password_hash):
		raise ValueError("Invalid email or password")
	if user.banned == 1:
		raise ValueError("User is banned")

	return encode_token(user.id)


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
