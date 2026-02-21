import asyncio
from sqlalchemy import insert
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))


from src.database import async_session_maker
from src.config import settings
from src.utils.users_utils import user_utils
from src.models.admin import AdminModel
from src.models.client import ClientModel

async def create_admin():
    async with async_session_maker() as session:
        stmt_admin = insert(AdminModel).values(
            login=settings.ADMIN_LOGIN,
            hashed_password=user_utils.hasheed_password(settings.ADMIN_PASSWORD),
            hashed_secret_word=user_utils.hasheed_password
        ).returning(AdminModel)
        result_stmt_admin = await session.execute(stmt_admin)
        admin = result_stmt_admin.scalar_one()
        stmt_client = insert(ClientModel).values(
            phone = settings.ADMIN_PHONE,
            id_user = admin.id,
            is_guest = False,
            rating = 0.0

        )
        await session.execute(stmt_client)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(create_admin())
