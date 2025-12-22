from sqlalchemy import delete,select
from sqlalchemy.orm import selectinload


from src.repository.base import BaseOrmRep
from src.repository.base_core import BaseCoreRep
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
    MasterSpecializationSchema,
    MasterDetailSchema
)



class MasterRepository(BaseOrmRep):
    model = MasterModel
    schema = MasterSchema

    async def get_master_by_id(self,id : int):
        query = (select(self.model)
                 .where(self.model.id == id)
                 .options(
                     selectinload(self.model.specialization),
                     selectinload(self.model.work_days),
                     selectinload(self.model.day_offs)
                 ))
        result = await self.session.execute(query)
        return MasterDetailSchema.model_validate(result.scalar_one(),from_attributes=True)


class SpecializationMasterRelationRepository(BaseCoreRep):
    table = master_specialization_table
    schema = SpecializationMasterRelationSchema

    async def delete_bulk_by_name_column_and_list_ids(self,id : int, list_ids : list[int]):
            stmt = delete(self.table).where(self.table.c.master_id == id, 
                                                                self.table.c.masterspecialization_id.in_(list_ids)).returning(self.table)
            result = await self.session.execute(stmt)
            return [self.schema.model_validate(model,from_attributes=True) for model in result.mappings().all()]
    


class MasterSpecializationRepository(BaseOrmRep):
    model = MasterSpecializationModel
    schema = MasterSpecializationSchema

    async def check_ids(self, ids_request : list[int]):
        ids_specialization = [model.id for model in await self.get_all()]
        if master_utils.all_ids_exist(ids_request = ids_request, ids_base = ids_specialization) is False:
            raise NoFound



class WorkDayRepository(BaseOrmRep):
    model = WorkDayModel
    schema = WorkDaySchema


class DayOffRepository(BaseOrmRep):
    model = DayOffModel
    schema = DayOffSchema


class MasterRequestRepository(BaseOrmRep):
    model = MasterRequestModel
    schema = MasterRequestSchema
