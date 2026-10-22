import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

database_url = make_url(os.environ["DATABASE_URL"].strip())

if database_url.drivername in (
    "postgres",
    "postgresql",
    "postgresql+psycopg2",
):
    database_url = database_url.set(drivername="postgresql+psycopg")

engine = create_engine(database_url, echo=False, pool_pre_ping=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass