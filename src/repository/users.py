from src.repository.base import BaseRep
from src.models.users import UsersModel
from src.schemas.users import User,UserDB,UserCreate
from src.utils.users_utils import converts_data

class UsersRepository(BaseRep):
    model = UsersModel
    schema = User
