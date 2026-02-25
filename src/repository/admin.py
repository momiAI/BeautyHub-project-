from sqlalchemy import select,join
from sqlalchemy.exc import NoResultFound

from src.repository.base import BaseOrmRep
from src.models.admin import AdminModel,AdminVerifyModel
from src.schemas.admin import AdminSchema, AdminVerifySchema,AdminVerifyAndPasswordsWithLoginSchema
from src.utils.exceptions import NoFound


class AdminRepository(BaseOrmRep):
    model = AdminModel
    schema = AdminSchema


class AdminVerifyRepository(BaseOrmRep):
    model = AdminVerifyModel
    schema = AdminVerifySchema

    async def get_full_admin(self,**kwargs) -> AdminVerifyAndPasswordsWithLoginSchema | None:
        query = (
            select(self.model,AdminModel.hashed_password,AdminModel.hashed_secret_word)
                 .join(AdminModel, self.model.admin_id == AdminModel.id) 
                 .filter_by(**kwargs)
                 )
        result = await self.session.execute(query)
        row = result.mappings().one_or_none()
        if row is not None:
            return AdminVerifyAndPasswordsWithLoginSchema(
                admin=self.schema.model_validate(row['AdminVerifyModel'],from_attributes=True),
                hashed_password=row['hashed_password'],
                hashed_secret_word=row['hashed_secret_word']
            )
        else:
            return None
