from src.models.enum import UserRoleEnum
from src.service.base import BaseService
from src.schemas.users import UserCreate, UserLogin,UserRoleUpdateSchema
from src.schemas.client import ClientUpdateUserSchema
from src.utils.users_utils import user_utils
from src.schemas.client import ClientDbSchema
from src.service.client import ClientService
from src.utils.exceptions import (
    UniqueError,
    UserUniqueError,
    IncorectPhone,
    NoFound,
    UserNoFound,
    IncorectData,
    IncorectToken,
)


class UsersService(BaseService):
    async def get_user_me(self, id: int):
        try:
            return await self.db.user.get_object(id=id)
        except NoFound:
            raise UserNoFound

    async def login_user(self, data: UserLogin):
        try:
            user = await self.db.user.get_object(
                phone=user_utils.validate_phone(data.phone)
            )
            if user_utils.verify_password(data.password, user.password_hash) is False:
                raise IncorectData
            client = await self.db.client.get_object_or_none(id_user = user.id)
            if user.role != UserRoleEnum.MASTER:
                return user_utils.create_access_refresh_tokens(id_user=user.id,role=user.role,id_client=client.id)
            else:
                master = await self.db.master.get_object(id_user = user.id)
                return user_utils.create_access_refresh_tokens(id_user=user.id,role=user.role,id_role=master.id,id_client=client.id)
        
        except NoFound:
            raise UserNoFound
        except IncorectPhone:
            raise IncorectPhone

    async def refresh_cookies(self, refresh_token):
        data = user_utils.decode_token(refresh_token=refresh_token)
        if data["type"] != "refresh":
            raise IncorectToken
        return user_utils.create_access_token(data)

    async def create_user(self, data: UserCreate):
        try:
            data_update = user_utils.converts_data(data)
            client = await self.db.client.get_object_or_none(phone = data_update.phone)
            user = await self.db.user.create(data_update)
            if client is None:
                await ClientService(self.db).create_client(phone = data_update.phone, id_user=user.id)
            else:
                await self.db.client.update(client.id,ClientUpdateUserSchema(id_user=user.id))
            return user
        except UniqueError:
            raise UserUniqueError
        except IncorectPhone:
            raise IncorectPhone

    async def delete_user(self, id: int):
        try:
            return await self.db.user.delete_by_id(id)
        except NoFound:
            raise UserNoFound

    async def replace_role_the_administrator(self,id : int):
        try:
            return await self.db.user.update(id,UserRoleUpdateSchema(role = UserRoleEnum.ADMINISTRATOR))
        except NoFound:
            raise UserNoFound