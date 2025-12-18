from src.repository.base import BaseOrmRep
from src.models.users import UsersModel
from src.schemas.users import User


class UsersRepository(BaseOrmRep):
    model = UsersModel
    schema = User
