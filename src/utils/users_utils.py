from pwdlib import PasswordHash

from src.schemas.users import UserDB,UserCreate

password_hash = PasswordHash.recommended()

async def hasheed_password(password):
    return password_hash.hash(password)


async def converts_data(data : UserCreate):
    return UserDB(
        phone = data.phone,
        name = data.name,
        password_hash = await hasheed_password(data.password),
        role = "client",
        rating = []
    )
    