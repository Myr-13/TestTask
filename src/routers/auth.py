from fastapi import APIRouter

from src.models.auth import LoginRequest, LoginResponse
from src.base.database import DATABASE
import src.controllers.auth as controller

router = APIRouter(
	prefix="/auth"
)


@router.post("/login", response_model=LoginResponse)
async def login(form: LoginRequest):
	print(DATABASE.engine)

	login_result = controller.login(
		email=form.email,
		password=form.password
	)

	if login_result is None:
		return LoginResponse(code=1, message="Email or password is wrong", auth_token=None)
	else:
		return LoginResponse(code=0, auth_token=login_result)


@router.post("/register")
async def register():
	pass
