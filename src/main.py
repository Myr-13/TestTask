from fastapi import FastAPI
import uvicorn
import argparse
import logging
import contextlib

from routers.auth import router

from base.config import CONFIG
from base.database import DATABASE


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
	logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

	parser = argparse.ArgumentParser(exit_on_error=False)
	parser.add_argument("--config", "-c", type=str, help="Path to config file")
	args = parser.parse_args()

	CONFIG.load_config(args.config)
	await DATABASE.open_connection(CONFIG["database_path"])
	print(CONFIG["database_path"])

	yield

	await DATABASE.close_connection()


app = FastAPI(lifespan=lifespan)

app.include_router(router)
