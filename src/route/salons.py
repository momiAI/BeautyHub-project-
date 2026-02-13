from fastapi import APIRouter,HTTPException

from src.route.dependency import DbDep
from src.service.salon import SalonService
from src.models.enum import CityEnum
from src.utils.exceptions import SalonNoFound

router = APIRouter(prefix='/salons', tags=['Салон'])


@router.get(path='', summary='Получить салоны с возможностью фильтрации по городам')
async def get_salons(db : DbDep, city : CityEnum | None = None):
    result = await SalonService(db).get_salons(city)
    return {'data' : result}

@router.get(path='/{id_salon}', summary='Получить салон по айди')
async def get_salon_by_id(db:DbDep, id_salon : int):
    try:
        result = await SalonService(db).get_salon_by_id(id_salon)
        return {'data' : result}
    except SalonNoFound as exc:
        raise HTTPException(status_code=404,detail=exc.detail)