from fastapi import APIRouter,Body,HTTPException,Response

from src.route.dependency import DbDep
from src.schemas.users import UserCreate,UserLogin
from src.service.users import UsersService
from src.utils.exceptions import IncorectPhone, UserUniqueError, UserNoFound,IncorectData


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


@router.post("/login", summary="Авторизация и аутенфикация")
async def user_login(db : DbDep, response : Response, data : UserLogin = Body(openapi_examples= {"1" : {
    "summary" : "Vlad",
    "value" : {
        "phone" : "+79394455771",
        "password" : "abcd1234"
    }
}})):
    try:
        access_token =  await UsersService(db).login_user(data)
        response.set_cookie("access_token",access_token)
        return {"message" : "OK"}
    except UserNoFound as exc:
        raise HTTPException(status_code=404, detail=exc.detail)
    except IncorectPhone as exc:
        raise HTTPException(status_code=400, detail=exc.detail)
    except IncorectData as exc:
        raise HTTPException(status_code=400, detail=exc.detail)


@router.post("/logout", summary="Удаление куков, выход")
async def user_logout(response : Response):
    response.delete_cookie("access_token")
    return {"message" : "OK"}


@router.delete("/delete", summary="Удалить пользователя")
async def user_delete(db : DbDep, id : int):
    try:
        result = await UsersService(db).delete_user(id)
        await db.commit()
        return {"data" : result}
    except UserNoFound as exc:
        raise HTTPException(status_code=404, detail=exc.detail)