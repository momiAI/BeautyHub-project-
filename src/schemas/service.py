from pydantic import BaseModel
from src.models.enum import CategoryEnum


class ServiceCreateSchemas(BaseModel):
    name: str
    category: CategoryEnum


class ServiceSchemas(ServiceCreateSchemas):
    id: int


class ServiceRelationSchema(BaseModel):
    service_id : int 
    masterspecialization_id : int 