from pydantic import BaseModel



class ServiceCreateSchemas(BaseModel):
    name : str
    price : int
    duration_minutes : int
    category : str


class ServiceSchemas(ServiceCreateSchemas):
    id : int
