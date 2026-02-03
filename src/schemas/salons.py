from pydantic import BaseModel

class SalonAddSchema(BaseModel):
    name : str
    city : str
    image_url : str

class SalonSchema(SalonAddSchema):
    id : int