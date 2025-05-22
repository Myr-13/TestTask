from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.models.schemas import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse, BooksResponse
import src.base.database as database
import src.controllers.books as controller

router = APIRouter(
	prefix="/books"
)


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
