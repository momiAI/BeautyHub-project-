from fastapi import APIRouter,Body

from src.route.dependency import MeDep,DbDep,AdminDep
from src.service.masters_specializations import MasterSpecializationService
from src.schemas.masters import MasterSpecializationCreateSchema

router = APIRouter(prefix="/master-specialization", tags=["Специализация мастеров"])


@router.get(path='/all', summary="Получить все специализации")
async def all_specialization(db : DbDep, user : MeDep):
    return await MasterSpecializationService(db).get_all()


@router.post(path='/add', summary="Добавление специализации")
async def add_specialization(db : DbDep, admin : AdminDep, data : MasterSpecializationCreateSchema = Body(openapi_examples={"1" : {
    "summary" : "Лашмейкер",
    "value" : {
        "name" : "Лашмейкер"
    }
}
})):
    result = await MasterSpecializationService(db).create(data)
    await db.commit()
    return {"data" : result}