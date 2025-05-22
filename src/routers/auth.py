from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.models.schemas import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
import src.base.database as database
import src.controllers.auth as controller

router = APIRouter(
	prefix="/auth"
)


def get_db():
	db = database.session_local()
	try:
		yield db
	finally:
		db.close()


@router.post("/login", response_model=LoginResponse)
async def login(form: LoginRequest, db: Session = Depends(get_db)):
	try:
		res = await controller.login(
			email=form.email,
			password=form.password,
			db=db
		)
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))

	return LoginResponse(code=0, auth_token=res)


@router.post("/register")
async def register(form: RegisterRequest, db: Session = Depends(get_db)):
	try:
		await controller.register(
			email=form.email,
			password=form.password,
			db=db
		)
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))

	return RegisterResponse(code=0, message="Account created successfully")
