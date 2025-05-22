import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base


engine: sqlalchemy.Engine = ...
session_local: sessionmaker = ...

Base = declarative_base()


def initialize_db(database_path: str) -> None:
	global engine, session_local

	engine = sqlalchemy.create_engine(f"sqlite:///{database_path}")
	session_local = sessionmaker(bind=engine, autocommit=False, autoflush=False)
