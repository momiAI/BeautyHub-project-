import asyncio
from typing import Annotated
from fastapi import Depends,Request,HTTPException


from src.schemas.users import UserDepSchema
from src.utils.exceptions import IncorectToken,TokenTimeIsOver
from src.utils.users_utils import user_utils
from src.utils.db_manager import DbManager
from src.database import async_session_maker
from src.models.enum import UserRoleEnum





async def get_token(request : Request):
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(status_code=401, detail="Пользователь не аутифицирован")
    return token


async def get_user(token : str = Depends(get_token)):
    try:
        return UserDepSchema.model_validate(user_utils.decode_token(access_token=token))
    except IncorectToken:
        raise HTTPException(status_code=401, detail="Неверный токен")
    except TokenTimeIsOver:
        raise HTTPException(status_code=401, detail="Срок токена истек")


async def get_admin(token : str = Depends(get_token)):
    user =  UserDepSchema.model_validate(user_utils.decode_token(access_token=token))
    try:
        if user.role != UserRoleEnum.ADMIN:
            raise HTTPException(status_code=403, detail="Недостаточно прав для выполнения запроса!")
        else:
            return UserDepSchema.model_validate(user)
    except IncorectToken:
        raise HTTPException(status_code=401, detail="Неверный токен")
    except TokenTimeIsOver:
        raise HTTPException(status_code=401, detail="Срок токена истек")


async def get_db():
    async with DbManager(async_session_maker) as db:
        yield db





DbDep = Annotated[DbManager, Depends(get_db)]
UserDep = Annotated[UserDepSchema, Depends(get_user)]
AdminDep = Annotated[UserDepSchema,Depends(get_admin)]