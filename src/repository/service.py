from src.repository.base import BaseOrmRep
from src.repository.base_core import BaseCoreRep
from src.models.service import ServiceModel,specialization_service
from src.schemas.service import ServiceSchemas,ServiceRelationSchema


class ServiceRepository(BaseOrmRep):
    model = ServiceModel
    schema = ServiceSchemas


class ServiceRelationMasterRepository(BaseCoreRep):
    table = specialization_service
    schema = ServiceRelationSchema