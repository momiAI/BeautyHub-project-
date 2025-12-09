from pydantic import BaseModel


class Rating(BaseModel):
    id_from : int
    id_to : int
    rating : int 

class UserDB(BaseModel):
    phone : str
    name : str
    password_hash : str
    role : str

class User(UserDB):
    id : int
    rating : list[Rating] = []

class UserCreate(BaseModel):
    phone : str
    name : str
    password : str