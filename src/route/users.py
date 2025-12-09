from fastapi import APIRouter,Body
from src.route.dependency import DbDep
from src.schemas.users import UserCreate
from src.service.users import UsersService


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
    return await UsersService(db).create_user(data)