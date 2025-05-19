from fastapi import FastAPI
import os
import logging
import contextlib

from routers.auth import router

from base.config import CONFIG
from base.database import create_database


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
	logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

	config = os.getenv("APP_CONFIG")
	CONFIG.load_config(config)
	create_database(CONFIG["database_path"])

	yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)
