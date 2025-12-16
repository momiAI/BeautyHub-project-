from src.repository.base import BaseRep
from src.models.service import ServiceModel
from src.schemas.service import ServiceSchemas


class ServiceRepository(BaseRep):
    model = ServiceModel
    schema = ServiceSchemas
