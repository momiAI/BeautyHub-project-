from fastapi import APIRouter, Body, HTTPException

from src.route.dependency import UserDep, DbDep, AdminDep, MasterDep
from src.schemas.masters import MasterCreateRequestSchema, MasterUpdateSchema
from src.schemas.workday import WorkDayRequstSchema
from src.service.masters import MastersService
from src.utils.exceptions import (
    CancleRequestAndColldownError,
    MasterRequestAlreadyInProgressError,
    MasterRequestCooldownError,
    MasterRequestUniqueError,
    RoleNotAllowedError,
    ApplicationNoFound,
    ApplicationApproved,
    MasterNoFound,
    IdSpecializationNoFound
)

router = APIRouter(prefix="/master", tags=["Мастера"])



@router.get(path="/me",summary="Получение мастера")
async def me(db : DbDep, master : MasterDep):
    result = await MastersService(db).get_me()


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


@router.post(
    path="/confirm/{id}", summary="Одобрение заявки на добавления мастера админом"
)
async def confirm_application(id: int, db: DbDep, admin: AdminDep):
    try:
        result = await MastersService(db).confirm(id)
        await db.commit()
        return {"data": result}
    except ApplicationNoFound as exc:
        raise HTTPException(status_code=404, detail=exc.detail)
    except ApplicationApproved as exc:
        raise HTTPException(status_code=409, detail=exc.detail)


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
        result = await MastersService(db).patch(master.user_id, data)
        return {"data" : result}
    except MasterNoFound as exc:
        return HTTPException(status_code=404, detail = exc.detail)
    except IdSpecializationNoFound as exc:
        return HTTPException(status_code=404,detail=exc.detail)
    