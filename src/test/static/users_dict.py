from src.models.enum import UserRoleEnum
from src.schemas.users import UserDB
from src.utils.users_utils import user_utils

hash_password = user_utils.hasheed_password('abcd1234')

array_users_data = [
    UserDB(
        phone = '76362233441',
        name = 'Client',
        password_hash= hash_password,
        role = UserRoleEnum.CLIENT
    ),
    UserDB(
        phone = '76362233442',
        name = 'Master',
        password_hash= hash_password,
        role = UserRoleEnum.MASTER
    ),
    UserDB(
        phone = '76362233443',
        name = 'Administrator',
        password_hash= hash_password,
        role = UserRoleEnum.ADMINISTRATOR
    ),
    UserDB(
        phone = '76362233444',
        name = 'Admin',
        password_hash= hash_password,
        role = UserRoleEnum.ADMIN
    ),
        UserDB(
        phone = '76362233445',
        name = 'Client for master',
        password_hash= hash_password,
        role = UserRoleEnum.ADMIN
    )
]