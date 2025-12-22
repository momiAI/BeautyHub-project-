from datetime import datetime
from pydantic import BaseModel

from src.models.enum import ReceptionStatusEnum


class ReceptionRequestSchema(BaseModel):
    id_master: int
    id_service: int
    date_time: datetime

class ReceptionCreateSchema(ReceptionRequestSchema):
    id_user: int
    status: ReceptionStatusEnum

class ReceptionSchema(ReceptionCreateSchema):
    id : int