from pydantic import BaseModel
from sqlalchemy import insert,delete

from src.database import Base



class BaseRep: 
    model : Base = None
    schema : BaseModel = None

    def __init__(self, session):
        self.session = session

    async def create(self,data : BaseModel):
        result = await self.session.execute(insert(self.model).values(**data.model_dump()).returning(self.model))
        return self.schema.model_validate(result.scalar_one())

    async def delete_by_id(self,id : int):
        result = await self.session.execute(delete(self.model).where(id == id).returning(self.model))
        return self.schema.model_validate(result.scalar_one())