from pydantic import BaseModel
from src.models.enum import CategoryEnum


class ServiceCreateSchemas(BaseModel):
    name : str
    price : int
    duration_minutes : int
    category : CategoryEnum


class ServiceSchemas(ServiceCreateSchemas):
    id : int
