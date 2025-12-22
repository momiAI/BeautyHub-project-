from fastapi import APIRouter,HTTPException

from src.route.dependency import DbDep
from src.service.service import ServService
from src.models.enum import CategoryEnum
from src.utils.exceptions import NoFound

router = APIRouter(prefix="/service", tags=["Услуги"])

@router.get(path='',summary="Все усглуги")
async def all_service(db : DbDep):
    result = await ServService(db).get_all_service()
    return {"data" : result}

@router.get(path='/{category}', summary="Все услуги по категориям")
async def all_service_by_category(db : DbDep, category : CategoryEnum):
    try:
        result = await ServService(db).get_all_service_by_category(category)
        return {"data" : result}
    except NoFound:
        raise HTTPException(status_code=404,detail="По данной категории услуги ещё не добавлены.")