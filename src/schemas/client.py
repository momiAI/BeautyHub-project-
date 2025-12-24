from pydantic import BaseModel


class ClientCreateSchema(BaseModel):
    phone : str

class ClientUpdateUserSchema(BaseModel):
    id_user : int 

class ClientDbSchema(ClientCreateSchema):
    id_user : int | None
    is_guest : bool
    rating : float


class ClientSchema(ClientDbSchema):
    id : int


class ClientRatingRelationSchema(BaseModel):
    id_from: int
    id_to: int
    rating: int
