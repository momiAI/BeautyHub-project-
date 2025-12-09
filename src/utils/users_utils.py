from pwdlib import PasswordHash

from src.schemas.users import User,UserCreate

password_hash = PasswordHash.recommended()

async def converts_data(data : UserCreate):
    