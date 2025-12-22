from src.repository.base import BaseOrmRep
from src.models.reception import ReceptionModel
from src.schemas.reception import ReceptionSchema

class ReceptionRepository(BaseOrmRep):
    model = ReceptionModel
    schema = ReceptionSchema
    