from datetime import datetime
from pydantic import BaseModel
from src.models.enum import UserRoleEnum


class Rating(BaseModel):
    id_from: int
    id_to: int
    rating: int


class UserDB(BaseModel):
    phone: str
    name: str
    password_hash: str
    role: UserRoleEnum


class UserRoleUpdateSchema(BaseModel):
    role: UserRoleEnum


class User(UserDB):
    id: int
    rating: list[Rating] = []
    last_update : datetime | None = None


class UserCreate(BaseModel):
    phone: str
    name: str
    password: str


class UserLogin(BaseModel):
    phone: str
    password: str


class UserDepSchema(BaseModel):
    client_id : int 
    user_id: int
    role: UserRoleEnum
    exp: int

class UserRequestUpdateSchema(BaseModel):
    phone : str | None = None
    name: str | None = None


class UserUpdateSchema(UserRequestUpdateSchema):
    last_update : datetime