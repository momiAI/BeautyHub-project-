from src.repository.base import BaseRep
from src.models.users import UsersModel
from src.schemas.users import User

class UsersRepository(BaseRep):
    model = UsersModel
    schema = User
