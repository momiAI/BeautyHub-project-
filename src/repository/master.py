from sqlalchemy import update


from src.repository.base import BaseRep
from src.models.master import MasterModel, MasterRequestModel, WorkDayModel, DayOffModel, master_specialization_table
from src.models.master_specialization import MasterSpecializationModel
from src.utils.masters_utils import master_utils
from src.utils.exceptions import NoFound
from src.schemas.masters import (
    MasterSchema,
    MasterRequestSchema,
    WorkDaySchema,
    DayOffSchema,
    SpecializationMasterRelationSchema,
    MasterSpecializationSchema
)



class MasterRepository(BaseRep):
    model = MasterModel
    schema = MasterSchema

    async def update_bio(self, id: int, value):
        result = await self.session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(bio=value)
            .returning(self.model)
        )
        return self.schema.model_validate(result.scalar_one(), from_attributes=True)


class SpecializationMasterRelationRepository(BaseRep):
    model = master_specialization_table
    schema = SpecializationMasterRelationSchema


class MasterSpecializationRepository(BaseRep):
    model = MasterSpecializationModel
    schema = MasterSpecializationSchema

    async def check_ids(self, ids_request : list[int]):
        ids_specialization = [model.id for model in await self.get_all()]
        if master_utils.all_ids_exist(ids_request = ids_request, ids_base = ids_specialization) is False:
            raise NoFound



class WorkDayRepository(BaseRep):
    model = WorkDayModel
    schema = WorkDaySchema


class DayOffRepository(BaseRep):
    model = DayOffModel
    schema = DayOffSchema


class MasterRequestRepository(BaseRep):
    model = MasterRequestModel
    schema = MasterRequestSchema
