import re
import jwt
from datetime import datetime,timedelta,timezone
from pwdlib import PasswordHash

from src.schemas.users import UserDB,UserCreate
from src.models.enum import UserRoleEnum
from src.utils.exceptions import IncorectPhone,IncorectToken,TokenTimeIsOver,TokenDublicate
from src.config import settings

password_hash = PasswordHash.recommended()

class UserUtils:

    def decode_token(self,access_token : str | None = None, refresh_token : str | None = None):
        try:
            if access_token:
                return jwt.decode(
                    access_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
                )
            elif refresh_token:
                return jwt.decode(
                    refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
                )
            else:
                raise TokenDublicate
        except jwt.exceptions.DecodeError:
            raise IncorectToken
        except jwt.exceptions.ExpiredSignatureError:
            raise TokenTimeIsOver


    def validate_phone(self,phone : str):
        PHONE_RE = re.compile(r'^7\d{10}$')
        digits = re.sub(r'\D', '', phone)
        if digits.startswith('8'):
            digits = '7' + digits[1:]
        if bool(PHONE_RE.fullmatch(digits)):
            return digits
        else:
            raise IncorectPhone 

    def create_access_token(self,data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire, "type" : "access"})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self,data: dict, expires_delta: timedelta = timedelta(days=30)):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire, "type" : "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def verify_password(self,plain_password, hashed_password):
        return password_hash.verify(plain_password, hashed_password)


    def hasheed_password(self,password):
        return password_hash.hash(password)


    def converts_data(self,data : UserCreate):
        phone = self.validate_phone(data.phone)
        return UserDB(
            phone = phone,
            name = data.name,
            password_hash = self.hasheed_password(data.password),
            role = UserRoleEnum.CLIENT.value,
            rating = []
        )

user_utils = UserUtils()