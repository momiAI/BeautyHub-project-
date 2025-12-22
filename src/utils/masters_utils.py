from datetime import datetime, timezone,date

from src.utils.exceptions import (
    MasterRequestCooldownError,
    MasterRequestUniqueError,
    CancleRequestAndColldownError,
    MasterRequestAlreadyInProgressError,
    IncorectData
)
from src.schemas.masters import (
    MasterConvertRequestSchema,
    MasterCreateRequestSchema,
    MasterRequestSchema,
    MasterDBSchema,
    SpecializationMasterRelationSchema,
)
from src.schemas.dayoff import DayOffCreateSchema,DayOffDBSchema
from src.models.enum import MasterRequestStatusEnum


class MastersUtils:
    def converts_request_data(self, id_user: int, data: MasterCreateRequestSchema):
        return MasterConvertRequestSchema(
            id_user=id_user,
            status=MasterRequestStatusEnum.PENDING,
            created_at=datetime.now().replace(second=0, microsecond=0),
            **data.model_dump(),
        )

    def converts_list_from_id_schema(self, master_id : int, ids_specialization : list[int]):
        return [
            SpecializationMasterRelationSchema(master_id=master_id,masterspecialization_id=i)
            for i in ids_specialization
        ]

    def converts_and_check_date_day_off(self, master_id : int ,data : DayOffCreateSchema):
        if data.day <  date.today():
            raise IncorectData
        return DayOffDBSchema(id_master=master_id,**data.model_dump())


    def converts_application(self, data: MasterRequestSchema):
        return MasterDBSchema(id_user=data.id_user, bio=data.bio_short)

    def check_application(self, application: MasterRequestSchema):
        delta = datetime.now(timezone.utc) - application.created_at
        if (
            application.status == MasterRequestStatusEnum.PENDING
            or application.status == MasterRequestStatusEnum.REJECTED
        ) and delta.days < 3:
            raise MasterRequestCooldownError

        elif application.status == MasterRequestStatusEnum.APPROVED:
            raise MasterRequestUniqueError

        elif application.status == MasterRequestStatusEnum.REJECTED and delta < 3:
            raise CancleRequestAndColldownError

        elif application.status == MasterRequestStatusEnum.IN_PROGRESS:
            raise MasterRequestAlreadyInProgressError

        else:
            return application

    def all_ids_exist(self,ids_request: list[int], ids_base: list[int]) -> bool:
        return set(ids_request).issubset(ids_base)

master_utils = MastersUtils()
