from fastapi import APIRouter, Body, HTTPException

from src.models.enum import ReceptionStatusEnum
from src.route.dependency import UserDep, DbDep, MasterDep
from src.schemas.masters import MasterCreateRequestSchema, MasterUpdateSchema
from src.schemas.dayoff import DayOffCreateSchema
from src.service.masters import MastersService
from src.service.reception import RecepionService
from src.utils.exceptions import (
    CancleRequestAndColldownError,
    MasterRequestAlreadyInProgressError,
    MasterRequestCooldownError,
    MasterRequestUniqueError,
    NoFound,
    RoleNotAllowedError,
    MasterNoFound,
    IdSpecializationNoFound,
    IncorectDate
)

router = APIRouter(prefix="/master", tags=["Мастера"])



@router.get(path="/me",summary="Получение мастера")
async def me(db : DbDep, master : MasterDep):
    try:
        return await MastersService(db).get_me(master.role_id)
    except MasterNoFound as exc:
        raise HTTPException(status_code=404,detail=exc.detail)


@router.post(path="/application", summary="Создание заявки на добавления мастера")
async def application(
    db: DbDep,
    user: UserDep,
    data: MasterCreateRequestSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Григорий",
                "value": {
                    "bio_short": "Профессионал своего дела",
                    "specializations": [
                        104,
                        105,
                        106
                    ],
                    "portfolio": ["Возможная ссылка", "Другая ссылка"],
                },
            }
        }
    ),
):
    try:
        result = await MastersService(db).request_application(
            id_user=user.user_id, data=data, role=user.role
        )
        await db.commit()
        return {"data": result}
    except MasterRequestCooldownError as exc:
        raise HTTPException(status_code=429, detail=exc.detail)
    except MasterRequestUniqueError as exc:
        raise HTTPException(status_code=409, detail=exc.detail)
    except CancleRequestAndColldownError as exc:
        raise HTTPException(status_code=429, detail=exc.detail)
    except MasterRequestAlreadyInProgressError as exc:
        raise HTTPException(status_code=409, detail=exc.detail)
    except RoleNotAllowedError:
        raise HTTPException(
            status_code=403, detail="Только пользователь может создать заявку."
        )
    except IdSpecializationNoFound as exc:
        raise HTTPException(status_code=404, detail=exc.detail)


@router.post(path="/day-off/add/",summary="Добавить выходной/отгул")
async def day_off_add(db : DbDep, master : MasterDep, data : DayOffCreateSchema = Body(openapi_examples={"1" : {"summary" : "Свадьба","value" : {
    "day": "2025-12-23",
    "reason": "У сестры свадьба"
}}})):
    try:
        result = await MastersService(db).add_day_off(master.role_id,data)
        await db.commit()
        return {"data" : result}
    except IncorectDate:
        raise HTTPException(status_code=422, detail="Прошлая дата, укажите настоящую или будущую дату.")

@router.patch(path="/update", summary="Обновление данных")
async def update_master(
    db: DbDep,
    master: MasterDep,
    data: MasterUpdateSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Полные данные",
                "value": {
                    "bio": "Cвоего дела",
                    "specialization": [
                        105,
                        106
                    ],
                    "workdays" : {
                        "day_of_week": ["monday","wednesday","friday"],
                        "start_time": "09:00",
                        "end_time": "18:00"
                    },
                },
            }
        }
    ),
):
    try:
        result = await MastersService(db).patch(master.role_id, data)
        await db.commit()
        return {"data" : result}
    except MasterNoFound as exc:
        return HTTPException(status_code=404, detail = exc.detail)
    except IdSpecializationNoFound as exc:
        return HTTPException(status_code=404,detail=exc.detail)

@router.patch(path="/master/cancel/{id_form}", summary="Отмена записи мастером")
async def cancel_recording(id_form : int,db : DbDep, master : MasterDep):
    try:
        result = await RecepionService(db).patch_status_form(id_form=id_form,id_master=master.role_id,status=ReceptionStatusEnum.CANCELLED_BY_MASTER)
        await db.commit()
        return {"data" : result}
    except NoFound:
        raise HTTPException(status_code=404, detail="Запись не найдена.")