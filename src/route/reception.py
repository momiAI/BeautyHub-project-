from fastapi import APIRouter,HTTPException

from src.schemas.reception import ReceptionRequestSchema
from src.route.dependency import DbDep, PhoneDep,UserDep,AministratorDep
from src.service.client import ClientService
from src.service.reception import RecepionService
from src.utils.exceptions import NoFound
from src.models.enum import ReceptionStatusEnum,ReceptionAdministraotStatusEnum

router = APIRouter(prefix="/reception", tags=["Ресепшн"])


@router.get(path="/search",summary="Получить клиента по номеру")
async def get_client(administrator : AministratorDep,db : DbDep, phone : PhoneDep):
    result = await ClientService(db).get_client(phone)
    return {"data" : result}


@router.post(path="/search",summary="Записать клиента")
async def get_client(administrator : AministratorDep, db : DbDep, phone : PhoneDep, data : ReceptionRequestSchema):
    result = await ClientService(db).record_client(phone,data)
    await db.commit()
    return {"data" : result}


@router.post(path="/create/",summary="Создать клиента")
async def get_client(administrator : AministratorDep,db : DbDep, phone : PhoneDep):
    result = await ClientService(db).create_client(phone)
    await db.commit()
    return {"data" : result}


@router.patch(path="/user/cancel/{id_form}", summary="Отмена записи клиентом")
async def cancel_recording(id_form : int,db : DbDep, user : UserDep):
    try:
        result = await RecepionService(db).patch_status_form(id_form=id_form,id_user=user.user_id,status=ReceptionStatusEnum.CANCELLED_BY_CLIENT)
        await db.commit()
        return {"data" : result}
    except NoFound:
        raise HTTPException(status_code=404, detail="Запись не найдена.")
    

@router.patch(path="/master/cancel/{id_form}", summary="Изменение статуса записи администратором")
async def cancel_recording(id_form : int,status : ReceptionAdministraotStatusEnum,db : DbDep, administrator : AministratorDep):
    try:
        result = await RecepionService(db).patch_status_form(id_form=id_form,status=status)
        await db.commit()
        return {"data" : result}
    except NoFound:
        raise HTTPException(status_code=404, detail="Запись не найдена.")