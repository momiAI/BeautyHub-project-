from src.repository.base import BaseOrmRep
from src.models.service import ServiceModel
from src.schemas.service import ServiceSchemas


class ServiceRepository(BaseOrmRep):
    model = ServiceModel
    schema = ServiceSchemas
