from pydantic import BaseModel
from sqlalchemy import insert,delete,select
from sqlalchemy.exc import IntegrityError,NoResultFound

from src.database import Base
from src.utils.exceptions import UniqueError,NoFound


class BaseRep: 
    model : Base = None
    schema : BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_object(self,**kwargs):
        try:
            result = await self.session.execute(select(self.model).filter_by(**kwargs))
            return self.schema.model_validate(result.scalar_one(),from_attributes=True)
        except NoResultFound:
            raise NoFound

    async def create(self,data : BaseModel):
        try:
            result = await self.session.execute(insert(self.model).values(**data.model_dump()).returning(self.model))
            return self.schema.model_validate(result.scalar_one(),from_attributes=True)
        except IntegrityError as exc:
            if getattr(exc.orig, "sqlstate", None) == "23505":
                raise UniqueError


    async def delete_by_id(self,id : int):
        try:
            result = await self.session.execute(delete(self.model).where(id == id).returning(self.model))
            return self.schema.model_validate(result.scalar_one(),from_attributes=True)
        except NoResultFound:
            raise NoFound