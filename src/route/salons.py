from fastapi import APIRouter

from src.route.dependency import DbDep
from src.service.salon import SalonService
from src.models.enum import CityEnum

router = APIRouter(prefix='/salons', tags=['Салон'])


@router.get(path='', summary='Получить салоны с возможностью фильтрации по городам')
async def get_salons(db : DbDep, city : CityEnum | None = None):
    result = await SalonService(db).get_salons(city)
    return {'data' : result}