from src.repository.base import BaseOrmRep
from src.repository.base_core import BaseCoreRep
from src.models.salons import SalonModel,master_salon
from src.schemas.salons import SalonSchema,SalonToMasterSchema


class SalonRepository(BaseOrmRep):
    model = SalonModel
    schema = SalonSchema


class SalonToMasterRepository(BaseCoreRep):
    table = master_salon
    schema = SalonToMasterSchema
