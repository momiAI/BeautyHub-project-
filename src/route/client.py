from fastapi import APIRouter

from src.route.dependency import PhoneDep,DbDep,AministratorDep
from src.service.client import ClientService
from src.schemas.reception import ReceptionRequestSchema



router = APIRouter(prefix="/client",tags=['Клиент'])


@router.get(path="/search",summary="Получить клиента по номеру")
async def get_client(administrator : AministratorDep,db : DbDep, phone : PhoneDep):
    result = await ClientService(db).get_client(phone)
    #await db.commit()
    return {"data" : result}

@router.post(path="/create/",summary="Создать клиента")
async def get_client(administrator : AministratorDep,db : DbDep, phone : PhoneDep):
    result = await ClientService(db).create_client(phone)
    #await db.commit()
    return {"data" : result}

@router.post(path="/search",summary="Записать клиента")
async def get_client(administrator : AministratorDep, db : DbDep, phone : PhoneDep, data : ReceptionRequestSchema):
    result = await ClientService(db).record_client(phone,data)
    #await db.commit()
    return {"data" : result}
    #перенести данную ручку в рецепшн а с оттуда в клиента... иначе путаница