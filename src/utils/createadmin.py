import asyncio
from sqlalchemy import insert
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))


from src.database import async_session_maker
from src.config import settings
from src.utils.users_utils import user_utils
from src.models.enum import UserRoleEnum
from src.models.users import UsersModel


async def create_admin():
    async with async_session_maker() as session:
        stmt = insert(UsersModel).values(
            phone=settings.ADMIN_PHONE,
            name="Super Admin",
            password_hash=user_utils.hasheed_password(settings.ADMIN_PASSWORD),
            role=UserRoleEnum.ADMIN,
        )
        await session.execute(stmt)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(create_admin())
