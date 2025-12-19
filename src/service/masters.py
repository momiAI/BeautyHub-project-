from src.service.base import BaseService
from src.schemas.users import UserUpdateMasterSchema
from src.schemas.masters import (
    MasterCreateRequestSchema,
    MasterRequestConfirmSchema,
    MasterUpdateSchema,
    SpecializationMasterRelationSchema,
    MasterBioUpdateSchema
)
from src.schemas.workday import WorkDayDbSchema,WorkDayRequstSchema
from src.utils.masters_utils import master_utils
from src.utils.exceptions import (
    MasterRequestAlreadyInProgressError,
    MasterRequestCooldownError,
    MasterRequestUniqueError,
    CancleRequestAndColldownError,
    NoFound,
    RoleNotAllowedError,
    ApplicationNoFound,
    MasterNoFound,
    ApplicationApproved,
    IdSpecializationNoFound
)
from src.models.enum import UserRoleEnum, MasterRequestStatusEnum


class MastersService(BaseService):
    async def request_application(
        self, id_user: int, data: MasterCreateRequestSchema, role: str
    ):
        data_update = master_utils.converts_request_data(id_user, data)
        
        if role != UserRoleEnum.CLIENT:
            raise RoleNotAllowedError
        
        try:
            await self.db.master_specialization.check_ids(data.specializations)
        except NoFound:
            raise IdSpecializationNoFound

        try:
            application = await self.db.master_request.get_object(id_user=id_user)
            if application:
                obj = master_utils.check_application(application)
                return await self.db.master_request.update(
                    id=obj.id, values=data_update
                )
        except MasterRequestCooldownError:
            raise MasterRequestCooldownError
        except MasterRequestUniqueError:
            raise MasterRequestUniqueError
        except CancleRequestAndColldownError:
            raise CancleRequestAndColldownError
        except MasterRequestAlreadyInProgressError:
            raise MasterRequestAlreadyInProgressError
        except NoFound:
            pass

        return await self.db.master_request.create(data_update)

    async def confirm(self, id: int):
        try:
            master_request = await self.db.master_request.get_object(id=id)
            if master_request.status == MasterRequestStatusEnum.APPROVED:
                raise ApplicationApproved
            application = master_utils.converts_application(master_request)
            await self.db.master_request.update(id, MasterRequestConfirmSchema())
            await self.db.user.update(application.id_user, UserUpdateMasterSchema())
            master =  await self.db.master.create(application)
            await self.db.master_specialization_relation.create_bulk(
                [
                    SpecializationMasterRelationSchema(master_id= master.id,masterspecialization_id=i)
                    for i in master_request.specializations
                ]
            )
            return master
        except NoFound:
            raise ApplicationNoFound

    async def patch(self, user_id: int, data: MasterUpdateSchema):
        
        try:
            master = await self.db.master.get_object(id_user=user_id) 
        except NoFound:
            raise MasterNoFound
        result = {}


        if data.bio:
            result["bio"] = await self.db.master.update(master.id, MasterBioUpdateSchema(bio = data.bio))


        if data.specialization:
            ids_base = [ids.masterspecialization_id for ids in await self.db.master_specialization_relation.get_all_by_name_column_id(master.id,"master_id")]
            if set(data.specialization).issubset(set(ids_base)) is False:
                raise IdSpecializationNoFound
            add_list_ids = list(set(data.specialization) - set(ids_base))
            delete_list_ids = list(set(ids_base) - set(data.specialization))
            add_list_schemas = master_utils.converts_list_from_id_schema(master_id=master.id,ids_specialization=add_list_ids)
                

        if delete_list_ids:
            result["ids_delete"] = await self.db.master_specialization_relation.delete_bulk_by_name_column_and_list_ids(master.id,delete_list_ids)


        if add_list_ids:
            result["ids_add"] = await self.db.master_specialization_relation.create_bulk(add_list_schemas)


        if data.workdays:
            try:
                check_in_db = await self.db.workday.get_object(id_master = master.id)
                result["workday"] = await self.db.workday.update(check_in_db.id,set(data.workdays))
            except NoFound:
                data_workday_update = WorkDayRequstSchema(
                    day_of_week=set(data.workdays.day_of_week),
                    start_time=data.workdays.start_time,
                    end_time=data.workdays.end_time
                    )
                result["workday"] = await self.db.workday.create(WorkDayDbSchema(id_master=master.id, **data_workday_update.model_dump())) 
                
        return result

