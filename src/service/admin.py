from src.service.base import BaseService
from src.schemas.admin import AdminLoginSchema,AdminVerifySchema,AdminCreateVerifySchema,AdminUpdateAttemptsSchema
from src.utils.users_utils import user_utils
from src.utils.date_utils import date_utils
from src.utils.exceptions import AdminNoFound, IncorectNowPassword, NoFound,RequestCooldownError

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
        admin_verify = await self.db.admin_verify.get_full_admin(data_login.login)
        if admin_verify.admin.attempts == 5:
            raise RequestCooldownError
        if admin_verify is None:
            try:
                admin = await self.db.admin.get_object(login = data_login.login)
            except NoFound:
                raise AdminNoFound
            admin_verify = await self.db.admin_verify.get_full_admin(admin.login)
        if not user_utils.verify_password(data_login.password,admin_verify.hashed_password):
            await self.db.admin_verify.update(admin_verify.admin.id, AdminUpdateAttemptsSchema(attempts=admin_verify.admin.attempts + 1))
            raise IncorectNowPassword
        return admin_verify.verify_token
        



