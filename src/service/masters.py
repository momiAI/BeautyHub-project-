from src.service.base import BaseService
from src.schemas.users import UserUpdateMasterSchema
from src.schemas.masters import (
    MasterCreateRequestSchema,
    MasterRequestConfirmSchema,
    MasterUpdateSchema,
)
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
            application = master_utils.converts_application(
                await self.db.master_request.get_object(id=id)
            )
            if application.status == MasterRequestStatusEnum.APPROVED:
                raise ApplicationApproved
            await self.db.master_request.update(id, MasterRequestConfirmSchema())
            await self.db.user.update(application.id_user, UserUpdateMasterSchema())
            return await self.db.master.create(application)
        except NoFound:
            raise ApplicationNoFound

    async def patch(self, user_id: int, data: MasterUpdateSchema):
        try:
            master = await self.db.master.get_object(id_user=user_id)
            if data.bio:
                await self.db.master.update_bio(master.id, data.bio)

        except NoFound:
            raise MasterNoFound
