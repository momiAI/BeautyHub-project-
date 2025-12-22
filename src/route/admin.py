from fastapi import APIRouter,Body, HTTPException,Depends

from src.route.dependency import AdminDep,DbDep
from src.schemas.masters import MasterSpecializationCreateSchema
from src.schemas.service import ServiceCreateSchemas
from src.service.masters import MastersService
from src.service.masters_specializations import MasterSpecializationService
from src.service.service import ServService
from src.service.users import UsersService
from src.utils.exceptions import ApplicationApproved, ApplicationNoFound, UserNoFound


router = APIRouter(prefix="/admin",tags=["Админ ручки"])


@router.post("/service-add", summary="Добавление услуг")
async def add_service(db : DbDep,admin : AdminDep, data : ServiceCreateSchemas = Body(openapi_examples= {"1" : {
    "summary" : "Наращивание ресниц",
    "value" : {
        "name": "Наращивание ресниц",
        "category": "lash"
    }
 }})):
    result = await ServService(db).create(data)
    await db.commit()
    return {"data" : result}


@router.post(
    path="/master/confirm/{id}", summary="Одобрение заявки на добавления мастера админом"
)
async def confirm_application(id: int,admin : AdminDep, db: DbDep):
    try:
        result = await MastersService(db).confirm(id)
        await db.commit()
        return {"data": result}
    except ApplicationNoFound as exc:
        raise HTTPException(status_code=404, detail=exc.detail)
    except ApplicationApproved as exc:
        raise HTTPException(status_code=409, detail=exc.detail)


@router.post(path='/specialization/add', summary="Добавление специализации")
async def add_specialization(db : DbDep,admin : AdminDep, data : MasterSpecializationCreateSchema = Body(openapi_examples={"1" : {
    "summary" : "Лашмейкер",
    "value" : {
        "name" : "Лашмейкер"
    }
}
})):
    result = await MasterSpecializationService(db).create(data)
    await db.commit()
    return {"data" : result}

@router.delete("/delete/user/{id}", summary="Удалить пользователя")
async def user_delete(db: DbDep, id: int, admin : AdminDep):
    try:
        result = await UsersService(db).delete_user(id)
        await db.commit()
        return {"data": result}
    except UserNoFound as exc:
        raise HTTPException(status_code=404, detail=exc.detail)
