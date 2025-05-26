from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.models.schemas import BooksResponse, BookBorrowRequest, BookReturnRequest
import src.base.database as database
import src.controllers.users as controller

router = APIRouter(
	prefix="/users"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
	db = database.session_local()
	try:
		yield db
	finally:
		db.close()


@router.get("/borrowed_books_list")
async def login(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
	try:
		res = await controller.get_books_list(token=token, db=db)
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))

	return res
