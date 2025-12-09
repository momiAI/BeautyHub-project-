from src.repository.base import BaseRep
from src.models.users import UsersModel
from src.schemas.users import User
from src.schemas.users import UserCreate

class UsersRepository(BaseRep):
    model = UsersModel
    schema = User

    async def create(self, data : UserCreate):
        pass
    #дописать схему для добавления в базу данных юзера 