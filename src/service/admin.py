from src.service.base import BaseService
from src.schemas.admin import AdminLoginSchema,AdminVerifySchema,AdminCreateVerifySchema
from src.utils.users_utils import user_utils
from src.utils.date_utils import date_utils
from src.utils.exceptions import AdminNoFound, IncorectNowPassword, NoFound

class AdminService(BaseService):

    async def _create_verify_obj(self,admin_id : int) -> AdminVerifySchema:
        create_data = AdminCreateVerifySchema(
            admin_id=admin_id,
            verify_token=user_utils.create_verify_token,
            expire_at=date_utils.create_expire_token,
            attempts=0,
            last_attempt=date_utils.now
        )
        return await self.db.admin_verify.create(create_data)


    async def login_admins(self,data_login : AdminLoginSchema) -> str:
        try:
            admin = await self.db.admin.get_object(login = data_login.login)
        except NoFound:
            raise AdminNoFound
        if not user_utils.verify_password(data_login.password,admin.hashed_password):
            raise IncorectNowPassword
        admin_verify = await self.db.admin_verify.get_object_or_none(admin_id = admin.id)
        if admin_verify is None:
            admin_verify = await self._create_verify_obj(admin_id=admin.id)
        return admin_verify.verify_token
        



