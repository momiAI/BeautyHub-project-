from pydantic import BaseModel
from datetime import datetime

from src.models.enum import MasterRequestStatusEnum
from src.schemas.users import UserDepSchema
from src.schemas.dayoff import DayOffCreateSchema
from src.schemas.workday import WorkDaySchema,WorkDayRequstSchema


class MasterSchema(BaseModel):
    id: int
    id_user: int
    bio: str

class MasterSpecializationCreateSchema(BaseModel):
    name : str


class MasterDetailSchema(MasterSchema):
    specialization: list[MasterSpecializationCreateSchema] | None = None
    work_days: list[WorkDaySchema] | None = None
    day_offs: list[DayOffCreateSchema] | None =None

class MasterBioUpdateSchema(BaseModel):
    bio : str


class MasterUpdateSchema(BaseModel):
    bio: str | None = None
    specialization: list[int] | None = None
    workdays : WorkDayRequstSchema
    day_off : DayOffCreateSchema

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


class MasterDepSchema(UserDepSchema):
    role_id : int 

class MasterSpecializationSchema(MasterSpecializationCreateSchema):
    id : int