from src.service.base import BaseService
from src.schemas.users import UserCreate
from src.utils.users_utils import converts_data

class UsersService(BaseService):
    async def create_user(self, data : UserCreate):
        data_update = await converts_data(data)
        return await self.db.user.create(data_update)