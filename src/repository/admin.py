from src.repository.base import BaseOrmRep
from src.models.admin import AdminModel,AdminVerifyModel
from src.schemas.admin import AdminSchema, AdminVerifySchema


class AdminRepository(BaseOrmRep):
    model = AdminModel
    schema = AdminSchema


class AdminVerifyRepository(BaseOrmRep):
    model = AdminVerifyModel
    schema = AdminVerifySchema