from typing import Annotated
from fastapi import Depends

from src.utils.db_manager import DbManager
from src.database import async_session_maker


async def get_db():
    async with DbManager(async_session_maker) as db:
        yield db

DbDep = Annotated[DbManager, Depends(get_db)]