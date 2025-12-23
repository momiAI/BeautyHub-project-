
from src.service.base import BaseService
from src.schemas.reception import ReceptionRequestSchema,ReceptionUpdateStatusSchema
from src.utils.reception_utils import reception_utils
from src.utils.exceptions import IncorectDate,IncorectData,ClientListUniqueError, NoFound
from src.models.enum import ReceptionStatusEnum

class RecepionService(BaseService):

    async def subscribe(self,id_user : int, data : ReceptionRequestSchema):
        check = await self.db.reception.get_object_or_none(id_user = id_user, id_master = data.id_master, date_time = data.date_time)
        if check is not None:
            raise ClientListUniqueError

        try: 
            data_update = reception_utils.check_date_and_convert_requst_data(id_user,data)
            return await self.db.reception.create(data_update)
        except IncorectData:
            raise IncorectDate

    async def patch_status_form(self,id_form : int,status : ReceptionStatusEnum,id_user : int | None = None, id_master : int | None = None):
        if id_user:
            check = await self.db.reception.get_object_or_none(id = id_form, id_user = id_user)
        if id_master:
            check = await self.db.reception.get_object_or_none(id = id_form, id_master = id_master)

        if check is None:
            raise NoFound
        
        return await self.db.reception.update(id_form, ReceptionUpdateStatusSchema(status= status))