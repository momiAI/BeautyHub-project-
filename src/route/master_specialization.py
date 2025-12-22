from fastapi import APIRouter

from src.route.dependency import MeDep,DbDep
from src.service.masters_specializations import MasterSpecializationService

router = APIRouter(prefix="/master-specialization", tags=["Специализация мастеров"])


@router.get(path='/all', summary="Получить все специализации")
async def all_specialization(db : DbDep, user : MeDep):
    return await MasterSpecializationService(db).get_all()
