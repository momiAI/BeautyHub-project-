from src.service.base import BaseService
from src.schemas.users import UserCreate,UserLogin
from src.utils.users_utils import converts_data,validate_phone,create_access_token,verify_password
from src.utils.exceptions import UniqueError,UserUniqueError,IncorectPhone,NoFound,UserNoFound,IncorectData


class UsersService(BaseService):

    async def login_user(self, data : UserLogin):
        try:
            user = await self.db.user.get_object(phone = await validate_phone(data.phone))
            if verify_password(data.password, user.password_hash) is False:
                raise IncorectData
            acces_token = await create_access_token(
                {
                "user_id" : user.id,
                "role" : user.role.value
                }
            )
            return acces_token
        except NoFound:
            raise UserNoFound
        except IncorectPhone:
            raise IncorectPhone


    async def create_user(self, data : UserCreate):
        try:
            data_update = await converts_data(data)
            return await self.db.user.create(data_update)
        except UniqueError:
            raise UserUniqueError
        except IncorectPhone:
            raise IncorectPhone
        

    async def delete_user(self,id : int):
        try:
            return await self.db.user.delete_by_id(id)
        except NoFound:
            raise UserNoFound
           
