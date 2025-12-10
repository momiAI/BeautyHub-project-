from fastapi import APIRouter,Body,HTTPException

from src.route.dependency import DbDep
from src.schemas.users import UserCreate
from src.service.users import UsersService
from src.utils.exceptions import IncorectPhone, UserUniqueError


router = APIRouter(prefix='/users', tags=["Пользователи"])

@router.post("/create",summary="Создание пользователя")
async def user_create(db : DbDep,data : UserCreate = Body(openapi_examples={"1" : {
    "summary" : "Vlad",
    "value" : {
        "phone" : "+79394455771",
        "name" : "Vlad",
        "password" : "abcd1234"
    }
}})):
    try:
        result = await UsersService(db).create_user(data)
        await db.commit()
        return {"data" : result}
    except UserUniqueError as exc:
        raise HTTPException(status_code=409,detail=exc.detail)
    except IncorectPhone as exc:
        raise HTTPException(status_code=400, detail=exc.detail)


@router.delete("/delete", summary="Удалить пользователя")
async def user_delete(db : DbDep, id : int):
    result = await UsersService(db).delete_user(id)
    await db.commit()
    return {"data" : result}