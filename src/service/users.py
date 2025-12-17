from src.service.base import BaseService
from src.schemas.users import UserCreate, UserLogin
from src.utils.users_utils import user_utils
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
            access_token = user_utils.create_access_token(
                {"user_id": user.id, "role": user.role}
            )
            refresh_token = user_utils.create_refresh_token(
                {"user_id": user.id, "role": user.role}
            )
            return access_token, refresh_token
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
            return await self.db.user.create(data_update)
        except UniqueError:
            raise UserUniqueError
        except IncorectPhone:
            raise IncorectPhone

    async def delete_user(self, id: int):
        try:
            return await self.db.user.delete_by_id(id)
        except NoFound:
            raise UserNoFound
