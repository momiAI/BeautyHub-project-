from fastapi import APIRouter, Body, HTTPException, Response, Cookie

from src.route.dependency import DbDep, MeDep
from src.schemas.users import UserCreate, UserLogin
from src.service.users import UsersService
from src.utils.exceptions import (
    IncorectPhone,
    UserUniqueError,
    UserNoFound,
    IncorectData,
)


router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("/me", summary="Получение пользователя")
async def user_me(db: DbDep, user: MeDep):
    try:
        result = await UsersService(db).get_user_me(user.user_id)
        return {"data": result}
    except UserNoFound as exc:
        raise HTTPException(status_code=404, detail=exc.detail)

        


@router.post("/create", summary="Создание пользователя")
async def user_create(
    db: DbDep,
    data: UserCreate = Body(
        openapi_examples={
            "1": {
                "summary": "Vlad",
                "value": {
                    "phone": "+79394455771",
                    "name": "Vlad",
                    "password": "abcd1234",
                },
            }
        }
    ),
):
    try:
        result = await UsersService(db).create_user(data)
        await db.commit()
        return {"data": result}
    except UserUniqueError as exc:
        raise HTTPException(status_code=409, detail=exc.detail)
    except IncorectPhone as exc:
        raise HTTPException(status_code=400, detail=exc.detail)


@router.post("/login", summary="Авторизация и аутенфикация")
async def user_login(
    db: DbDep,
    response: Response,
    data: UserLogin = Body(
        openapi_examples={
            "1": {
                "summary": "Vlad",
                "value": {"phone": "+79394455771", "password": "abcd1234"},
            },
            "2": {
                "summary": "Admin",
                "value": {"phone": "+79493322661", "password": "abcde1234"},
            }
        }
    ),
):
    try:
        access_token, refresh_token = await UsersService(db).login_user(data)
        response.set_cookie("access_token", access_token, httponly=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True)
        return {"message": "OK"}
    except UserNoFound as exc:
        raise HTTPException(status_code=404, detail=exc.detail)
    except IncorectPhone as exc:
        raise HTTPException(status_code=400, detail=exc.detail)
    except IncorectData as exc:
        raise HTTPException(status_code=400, detail=exc.detail)


@router.post("/refresh", summary="Обновление куков")
async def refresh_cookies(response: Response, refresh_token: str = Cookie(None)):
    new_access_token = await UsersService().refresh_cookies(refresh_token)
    response.set_cookie("access_token", new_access_token, httponly=True)
    return {"message": "OK"}


@router.post("/logout", summary="Удаление куков, выход")
async def user_logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "OK"}


@router.delete("/delete/{id}", summary="Удалить авторизированого пользователя")
async def user_delete(db: DbDep, user : MeDep):
    try:
        result = await UsersService(db).delete_user(user.user_id)
        await db.commit()
        return {"data": result}
    except UserNoFound as exc:
        raise HTTPException(status_code=404, detail=exc.detail)
