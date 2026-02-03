from src.repository.base import BaseOrmRep
from src.models.salons import SalonModel
from src.schemas.salons import SalonSchema


class SalonRepository(BaseOrmRep):
    model = SalonModel
    schema = SalonSchema