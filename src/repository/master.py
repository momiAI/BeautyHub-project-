from sqlalchemy import select,update


from src.repository.base import BaseRep
from src.models.master import MasterModel,MasterRequestModel,WorkDayModel,DayOffModel
from src.schemas.masters import MasterSchema,MasterRequestSchema,WorkDaySchema,DayOffSchema

class MasterRepository(BaseRep):
    model = MasterModel
    schema = MasterSchema

    async def update_bio(self,id : int,value):
        result = await self.session.execute(update(self.model).where(self.model.id == id).values(bio = value).returning(self.model))
        return self.schema.model_validate(result.scalar_one(),from_attributes=True)

class WorkDayRepository(BaseRep):
    model = WorkDayModel
    schema = WorkDaySchema
    

class DayOffRepository(BaseRep):
    model = DayOffModel
    schema = DayOffSchema


class MasterRequestRepository(BaseRep):
    model = MasterRequestModel
    schema = MasterRequestSchema