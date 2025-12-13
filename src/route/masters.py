from fastapi import APIRouter,Body,HTTPException

from src.route.dependency import UserDep,DbDep,AdminDep
from src.schemas.masters import MasterCreateRequestSchema
from src.service.masters import MastersService
from src.utils.exceptions import CancleRequestAndColldownError, MasterRequestAlreadyInProgressError, MasterRequestCooldownError, MasterRequestUniqueError

router = APIRouter(prefix="/master", tags=["Мастера"])

@router.post(path="/application", summary="Создание заявки на добавления мастера")
async def application(db : DbDep, user : UserDep,data : MasterCreateRequestSchema = Body(openapi_examples={"1" : {
    "summary" : "Григорий",
    "value" : {
        "bio_short" : "Профессионал своего дела",
        "specializations" : [
            'face',
            'hair' ,
            'nails' ,
            'lash' ,
            'brows',
            'depilation'
        ],
        "portfolio" : ["Возможная ссылка","Другая ссылка"]

    }
}})):
    try:
        result = await MastersService(db).request_application(id_user=user.user_id,data=data)
        await db.commit()
        return {"data" : result}
    except MasterRequestCooldownError as exc:
        raise HTTPException(status_code=429,detail=exc.detail)
    except MasterRequestUniqueError as exc:
        raise HTTPException(status_code=409,detail=exc.detail)
    except CancleRequestAndColldownError as exc:
        raise HTTPException(status_code=429,detail=exc.detail)
    except MasterRequestAlreadyInProgressError as exc:
        raise HTTPException(status_code=409, detail=exc.detail)


@router.post(path="/confirm/{id}",summary="Одобрение заявки на добавления мастера админом")
async def confirm_application(id : int, db : DbDep, admin : AdminDep):
    result = await MastersService(db).confirm(id)
    await db.commit()
    return {"data" : result}