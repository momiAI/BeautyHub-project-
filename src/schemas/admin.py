from datetime import datetime
from pydantic import BaseModel

from src.models.enum import UserRoleEnum

class AdminSchema(BaseModel):
    id : int
    login : str
    hashed_password : str
    role : str = UserRoleEnum.ADMIN.value
    hashed_secret_word : str

class AdminVerifySchema(BaseModel):
    id : int
    admin_id : int
    verify_token : str
    expire_at : datetime
    attempts : int
    last_attempt : datetime