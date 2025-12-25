from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from .config import settings
from sqlalchemy import NullPool
from sqlalchemy.orm import DeclarativeBase

if settings.MODE == "TEST":
    pool = {"poolclass": NullPool}
else:
    pool = {}

engine = create_async_engine(settings.db_url, **pool)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
