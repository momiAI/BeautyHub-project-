from sqlalchemy import update


from src.repository.base import BaseRep
from src.models.master import MasterModel, MasterRequestModel, WorkDayModel, DayOffModel, master_specialization_table
from src.schemas.masters import (
    MasterSchema,
    MasterRequestSchema,
    WorkDaySchema,
    DayOffSchema,
    SpecializationMasterSchema
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


class SpecializationMasterRepository(BaseRep):
    model = master_specialization_table
    schema = SpecializationMasterSchema

    async def add_bulk(self, master_id : int, specializations : list):
        dict_update = {"master_id" }


class WorkDayRepository(BaseRep):
    model = WorkDayModel
    schema = WorkDaySchema


class DayOffRepository(BaseRep):
    model = DayOffModel
    schema = DayOffSchema


class MasterRequestRepository(BaseRep):
    model = MasterRequestModel
    schema = MasterRequestSchema
