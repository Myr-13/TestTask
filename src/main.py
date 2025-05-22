from fastapi import FastAPI
import os
import logging
import contextlib

from routers.auth import router as auth_router
from routers.books import router as books_router

import src.base.config as config
import src.base.database as database
from src.models.models import User, Book, BorrowedBook


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
	logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

	config_path = os.getenv("APP_CONFIG")
	config.CONFIG.load_config(config_path)
	database.initialize_db(config.CONFIG["database_path"])

	User.metadata.create_all(bind=database.engine)
	Book.metadata.create_all(bind=database.engine)
	BorrowedBook.metadata.create_all(bind=database.engine)

	yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(books_router)
