from datetime import datetime
from pydantic import BaseModel

from src.models.enum import UserRoleEnum

class AdminSchema(BaseModel):
    id : int
    login : str
    hashed_password : str
    role : str = UserRoleEnum.ADMIN.value
    hashed_secret_word : str

class AdminUpdateAttemptsSchema(BaseModel):
    attempts : int

class AdminCreateVerifySchema(AdminUpdateAttemptsSchema):
    admin_id : int
    verify_token : str
    expire_at : datetime
    last_attempt : datetime


class AdminVerifySchema(AdminCreateVerifySchema):
    id : int


class AdminVerifyAndPasswordsWithLoginSchema(BaseModel):
    admin : AdminVerifySchema
    hashed_password : str
    hashed_secret_word : str
    

class AdminLoginSchema(BaseModel):
    login : str
    password : str