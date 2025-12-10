import re
import jwt
from datetime import datetime,timedelta,timezone
from pwdlib import PasswordHash

from src.schemas.users import UserDB,UserCreate
from src.models.enum import UserRoleEnum
from src.utils.exceptions import IncorectPhone
from src.config import settings

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

async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


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
    