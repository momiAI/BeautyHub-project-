import re
from pwdlib import PasswordHash

from src.schemas.users import UserDB,UserCreate
from src.models.enum import UserRoleEnum
from src.utils.exceptions import IncorectPhone

password_hash = PasswordHash.recommended()


async def validate_phone(phone : str):
    PHONE_RE = re.compile(r'^7\d{10}$')
    digits = re.sub(r'\D', '', phone)
    if digits.startswith('8'):
        digits = '7' + digits[1:]
    if bool(PHONE_RE.fullmatch(digits)):
        return digits
    else:
        raise IncorectPhone 


async def hasheed_password(password):
    return password_hash.hash(password)


async def converts_data(data : UserCreate):
    phone = await validate_phone(data.phone)
    return UserDB(
        phone = phone,
        name = data.name,
        password_hash = await hasheed_password(data.password),
        role = UserRoleEnum.CLIENT,
        rating = []
    )
    