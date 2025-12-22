from datetime import datetime ,timezone

from src.models.enum import ReceptionStatusEnum
from src.schemas.reception import ReceptionCreateSchema,ReceptionRequestSchema
from src.utils.exceptions import IncorectData

class ReceptionUtils:

    def check_date_and_convert_requst_data(self,id_user : int, data : ReceptionRequestSchema):
        if data.date_time > datetime.now():
            raise IncorectData
        return ReceptionCreateSchema(id_user=id_user,
                                     status=ReceptionStatusEnum.PENDING,
                                     **data.model_dump()
                                     )

reception_utils = ReceptionUtils()