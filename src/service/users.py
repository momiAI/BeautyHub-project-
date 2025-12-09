from src.service.base import BaseService
from src.schemas.users import UserCreate

class UsersService(BaseService):
    async def create_user(self, data : UserCreate):
        return await self.db.user.create(data)