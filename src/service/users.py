from src.service.base import BaseService
from src.schemas.users import UserCreate
from src.utils.users_utils import converts_data
from src.utils.exceptions import UniqueError,UserUniqueError,IncorectPhone

class UsersService(BaseService):

    async def create_user(self, data : UserCreate):
        try:
            data_update = await converts_data(data)
            return await self.db.user.create(data_update)
        except UniqueError:
            raise UserUniqueError
        except IncorectPhone:
            raise IncorectPhone
        

    async def delete_user(self,id : int):
        result = await self.db.user.delete_by_id(id)
        await self.db.commit()
        return result
