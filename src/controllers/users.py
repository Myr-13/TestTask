from sqlalchemy.orm import Session
from datetime import datetime

from src.models.models import BorrowedBook, User, UserRights
from src.models.schemas import BorrowedBookObject, UserObject
from src.controllers.auth import check_token, user_have_role


async def get_books_list(*, token: str, db: Session) -> list[BorrowedBook]:
	user_id: int = check_token(token)

	books_set = db.query(BorrowedBook).filter(BorrowedBook.user_id == user_id, BorrowedBook.return_date == None)
	out = []

	for book in books_set:
		book: BorrowedBook

		out.append(BorrowedBookObject(
			id=book.id,
			book_id=book.book_id,
			borrow_date=datetime.fromtimestamp(book.borrow_date)
		))

	return out


async def get_user_info(*, target_id: int, token: str, db: Session) -> UserObject:
	user_id: int = check_token(token)

	# Get authed user
	authed_user: User | None = db.query(User).filter(User.id == user_id).first()
	if authed_user is None:
		raise ValueError("Invalid token. User not found")

	# Check for rights
	if not user_have_role(authed_user, UserRights.GetUsersInfo):
		raise ValueError("Not enough rights")

	# Get target user data
	target_user: User | None = db.query(User).filter(User.id == target_id).first()
	if target_user is None:
		raise ValueError("Target user not found")

	return UserObject(
		id=target_user.id,
		email=target_user.email,
		rights=target_user.rights,
		banned=bool(target_user.banned)
	)
