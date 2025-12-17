from fastapi import APIRouter,Body

from src.route.dependency import AdminDep,DbDep
from src.service.service import ServService
from src.schemas.service import ServiceCreateSchemas

router = APIRouter(prefix="/service", tags=["Услуги"])



@router.post("/add", summary="Добавление услуг")
async def add_service(db : DbDep, admin : AdminDep, data : ServiceCreateSchemas = Body(openapi_examples= {"1" : {
    "summary" : "Наращивание ресниц",
    "value" : {
        "name": "Наращивание ресниц",
        "category": "lash"
    }
 }})):
    result = await ServService(db).create(data)
    await db.commit()
    return {"data" : result}