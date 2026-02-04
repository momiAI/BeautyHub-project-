from pydantic import BaseModel

class SalonAddSchema(BaseModel):
    name : str
    city : str
    address : str
    image_url : str | None = None

class SalonSchema(SalonAddSchema):
    id : int

class SalonUpdateSchema(BaseModel):
    name : str | None = None
    city : str | None = None
    image_url : str | None = None
    address : str | None = None
