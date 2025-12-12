from pydantic import BaseModel
from datetime import datetime

from src.models.enum import MasterRequestStatusEnum
from src.schemas.service import ServiceSchemas
from src.schemas.dayoff import DayOffSchema
from src.schemas.workday import WorkDaySchema


class MasterSchema(BaseModel):
    id : int 
    id_user : int
    bio : str

    specialization : list[ServiceSchemas]
    work_days : list[WorkDaySchema]
    day_offs : list[DayOffSchema]


class MasterCreateRequestSchema(BaseModel):
    bio_short : str
    specializations : list[str]
    portfolio : list[str]

class MasterConvertRequestSchema(MasterCreateRequestSchema):
    id_user : int 
    status : MasterRequestStatusEnum
    created_at : datetime 

class MasterRequestSchema(MasterConvertRequestSchema):
    id : int 










