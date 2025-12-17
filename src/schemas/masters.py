from pydantic import BaseModel
from datetime import datetime

from src.models.enum import MasterRequestStatusEnum, CategoryEnum
from src.schemas.service import ServiceSchemas
from src.schemas.dayoff import DayOffSchema
from src.schemas.workday import WorkDaySchema, WeekDayEnum


class MasterSchema(BaseModel):
    id: int
    id_user: int
    bio: str


class MasterDetailSchema(MasterSchema):
    specialization: list[ServiceSchemas]
    work_days: list[WorkDaySchema]
    day_offs: list[DayOffSchema]


class MasterUpdateSchema(BaseModel):
    bio: str | None = None
    specialization: list[int] | None = None
    work_days: list[WeekDayEnum] | None = None


class MasterDBSchema(BaseModel):
    id_user: int
    bio: str


class MasterCreateRequestSchema(BaseModel):
    bio_short: str
    specializations: list[int]
    portfolio: list[str]


class MasterConvertRequestSchema(MasterCreateRequestSchema):
    id_user: int
    status: MasterRequestStatusEnum
    created_at: datetime


class MasterRequestSchema(MasterConvertRequestSchema):
    id: int


class MasterRequestConfirmSchema(BaseModel):
    status: MasterRequestStatusEnum = MasterRequestStatusEnum.APPROVED


class SpecializationMasterRelationSchema(BaseModel):
    master_id : int 
    masterspecialization_id : int

class MasterSpecializationCreateSchema(BaseModel):
    name : str

class MasterSpecializationSchema(MasterSpecializationCreateSchema):
    id : int