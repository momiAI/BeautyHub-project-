from fastapi import APIRouter, Body, HTTPException

from src.models.enum import ReceptionStatusEnum
from src.route.dependency import PhoneDep,DbDep,AministratorDep,MeDep
from src.service.client import ClientService
from src.schemas.reception import ReceptionRequestSchema
from src.service.reception import RecepionService
from src.utils.exceptions import ClientListUniqueError, IncorectDate, NoFound



router = APIRouter(prefix="/client",tags=['Клиент'])



@router.post(path="/subscribe/",summary="Записаться к мастеру")
async def subscribe_to_master(db : DbDep,user : MeDep,data : ReceptionRequestSchema = Body(openapi_examples={"1" : {
    "summary" : "Записаться",
    "value" : {
        "id_master": 29,
        "id_service": 14,
        "date_time": "2025-12-22T14:30:00"
    }
}})):
    try:
        result = await RecepionService(db).subscribe(user.client_id,data)
        await db.commit()
        return {"data" : result}
    except IncorectDate:
        raise HTTPException(status_code=422, detail="Прошлая дата, укажите настоящую или будущую дату.")
    except ClientListUniqueError as exc:
        raise HTTPException(status_code=409, detail=exc.detail)
    

@router.patch(path="/cancel/{id_form}", summary="Отмена записи клиентом")
async def cancel_recording(id_form : int,db : DbDep, user : MeDep):
    try:
        result = await RecepionService(db).patch_status_form(id_form=id_form,id_client=user.client_id,status=ReceptionStatusEnum.CANCELLED_BY_CLIENT)
        await db.commit()
        return {"data" : result}
    except NoFound:
        raise HTTPException(status_code=404, detail="Запись не найдена.")