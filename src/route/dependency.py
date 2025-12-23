from typing import Annotated
from fastapi import Depends, Request, HTTPException


from src.schemas.users import UserDepSchema
from src.schemas.masters import MasterDepSchema
from src.utils.exceptions import IncorectToken, TokenTimeIsOver
from src.utils.users_utils import user_utils
from src.utils.db_manager import DbManager
from src.database import async_session_maker
from src.models.enum import UserRoleEnum


async def get_token(request: Request):
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(status_code=401, detail="Пользователь не аутифицирован")
    return token


def user_dependency(role: UserRoleEnum | None = None):
    async def get_user(token: str = Depends(get_token)):
        try:
            user = UserDepSchema.model_validate(
                user_utils.decode_token(access_token=token)
            )
            if role:
                if role != user.role:
                    print(role, user.role)
                    raise HTTPException(
                        status_code=403,
                        detail="Недостаточно прав для выполнения запроса!",
                    )
                if user.role == UserRoleEnum.MASTER:
                    return MasterDepSchema.model_validate(
                        user_utils.decode_token(access_token=token)
                    )
            return user
        except IncorectToken:
            raise HTTPException(status_code=401, detail="Неверный токен")
        except TokenTimeIsOver:
            raise HTTPException(status_code=401, detail="Срок токена истек")

    return get_user


async def get_db():
    async with DbManager(async_session_maker) as db:
        yield db


DbDep = Annotated[DbManager, Depends(get_db)]
MeDep = Annotated[UserDepSchema, Depends(user_dependency())]
UserDep = Annotated[UserDepSchema, Depends(user_dependency(UserRoleEnum.CLIENT))]
AdminDep = Annotated[UserDepSchema, Depends(user_dependency(UserRoleEnum.ADMIN))]
MasterDep = Annotated[UserDepSchema, Depends(user_dependency(UserRoleEnum.MASTER))]
AministratorDep = Annotated[UserDepSchema,Depends(user_dependency(UserRoleEnum.ADMINISTRATOR))]
