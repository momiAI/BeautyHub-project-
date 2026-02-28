from src.service.base import BaseService
from src.schemas.admin import AdminLoginSchema,AdminVerifySchema,AdminUpdateAttemptsSchema,AdminUpdateSchema,AdminSchema,AdminCreateVerifySchema,AdminVerifyAndPasswordsWithLoginSchema
from src.utils.users_utils import user_utils
from src.utils.date_utils import date_utils
from src.utils.exceptions import AdminNoFound, IncorectNowPassword, NoFound,RequestCooldownError, SessionExpired,IncorectToken,IncorectSecretWord

class AdminService(BaseService):

    async def _create_verify_obj(self,admin : AdminSchema) -> AdminVerifySchema:
        create_data = AdminCreateVerifySchema(
            admin_id=admin.id,
            verify_token=user_utils.create_verify_token,
            expire_at=date_utils.create_expire_token,
            attempts=0,
            last_attempt=date_utils.now
        )
        verify_schema = await self.db.admin_verify.create(create_data)
        return AdminVerifyAndPasswordsWithLoginSchema( admin=verify_schema,
                                                      hashed_password=admin.hashed_password,
                                                      hashed_secret_word=admin.hashed_secret_word )


    async def login_admins(self,data_login : AdminLoginSchema) -> str:
        admin_verify = await self.db.admin_verify.get_full_admin(login = data_login.login)
        if admin_verify is None:
            try:
                admin = await self.db.admin.get_object(login = data_login.login)
                admin_verify = await self._create_verify_obj(admin)
            except NoFound:
                raise AdminNoFound
        if admin_verify.admin.attempts >= 5:
            if date_utils.check_last_atempt(admin_verify.admin.last_attempt):
                await self.db.admin_verify.update(admin_verify.admin.id, AdminUpdateSchema(attempts=0, last_attempt=date_utils.now))
            else:
                raise RequestCooldownError
        if not user_utils.verify_password(data_login.password,admin_verify.hashed_password):
            await self.db.admin_verify.update(admin_verify.admin.id, AdminUpdateSchema(attempts=admin_verify.admin.attempts + 1, last_attempt=date_utils.now))
            raise IncorectNowPassword
        else:
            token = admin_verify.admin.verify_token
            await self.db.admin_verify.update(admin_verify.admin.id,AdminUpdateSchema(
                verify_token=token,
                last_attempt=date_utils.now,
                attempts=0,
                expire_at=date_utils.create_expire_token
                ) )
            return token
        

    async def verify_secret_word(self,token : str,secret_word : str) -> str:
        admin_verify = await self.db.admin_verify.get_full_admin(verify_token = token)
        if admin_verify is None:
            raise AdminNoFound
        if date_utils.now > admin_verify.admin.expire_at:
            raise SessionExpired
        if token != admin_verify.admin.verify_token:
            raise IncorectToken
        if not user_utils.verify_password(secret_word,admin_verify.hashed_secret_word):
            raise IncorectSecretWord
        await self.db.admin_verify.update(admin_verify.admin.id, AdminUpdateAttemptsSchema(attempts=0))
        return user_utils.create_access_admin_token(admin_verify.admin.admin_id)




