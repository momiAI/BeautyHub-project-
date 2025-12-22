from fastapi import APIRouter,Body,HTTPException

from src.schemas.reception import ReceptionRequestSchema
from src.route.dependency import DbDep,UserDep
from src.service.reception import RecepionService
from src.utils.exceptions import IncorectDate

router = APIRouter(prefix="/reception", tags=["Ресепшн","Действия с записями"])


@router.post(path="/subscribe/",summary="Записаться к мастеру")
async def subscribe_to_master(db : DbDep,user : UserDep,data : ReceptionRequestSchema = Body(openapi_examples={"1" : {
    "summary" : "Записаться",
    "value" : {
        "id_master": 29,
        "id_service": 14,
        "date_time": "2025-12-22T14:30:00"
    }
}})):
    try:
        result = await RecepionService(db).subscribe(user.user_id,data)
        await db.commit()
        return {"data" : result}
    except IncorectDate:
        raise HTTPException(status_code=422, detail="Прошлая дата, укажите настоящую или будущую дату.")