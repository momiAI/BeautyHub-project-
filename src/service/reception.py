
from src.service.base import BaseService
from src.schemas.reception import ReceptionRequestSchema
from src.utils.reception_utils import reception_utils
from src.utils.exceptions import IncorectDate,IncorectData


class RecepionService(BaseService):

    async def subscribe(self,id_user : int, data : ReceptionRequestSchema):
        try: 
            data_update = reception_utils.check_date_and_convert_requst_data(id_user,data)
            return await self.db.reception.create(data_update)
        except IncorectData:
            raise IncorectDate
