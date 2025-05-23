from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.models.schemas import BooksResponse, BookBorrowRequest
import src.base.database as database
import src.controllers.books as controller

router = APIRouter(
	prefix="/books"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
	db = database.session_local()
	try:
		yield db
	finally:
		db.close()


@router.get("/list", response_model=BooksResponse)
async def login(db: Session = Depends(get_db)):
	try:
		res = await controller.get(db=db)
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))

	return BooksResponse(books=res)


@router.post("/borrow", response_model=BooksResponse)
async def login(
		form: BookBorrowRequest,
		db: Session = Depends(get_db),
		token: str = Depends(oauth2_scheme)):

	try:
		res = await controller.borrow(token=token, book_id=form.book_id, db=db)
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))

	return BooksResponse(books=res)
