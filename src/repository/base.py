from pydantic import BaseModel
from sqlalchemy import insert, delete, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound,MultipleResultsFound

from src.database import Base
from src.utils.exceptions import UniqueError, NoFound, MultipleResult


class BaseOrmRep:
    model: Base = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(select(self.model))
        return [self.schema.model_validate(model,from_attributes=True) for model in result.scalars().all()]
    

    async def get_all_by_filters(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model,from_attributes=True) for model in result.scalars().all()]
    

    async def get_object(self, **kwargs):
        try:
            result = await self.session.execute(select(self.model).filter_by(**kwargs))
            return self.schema.model_validate(result.scalar_one(), from_attributes=True)
        except NoResultFound:
            raise NoFound
        except MultipleResultsFound:
            raise MultipleResult
    
    async def update(self, id: int, values: BaseModel):
        result = await self.session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**values.model_dump())
            .returning(self.model)
        )
        return self.schema.model_validate(result.scalar_one(), from_attributes=True)

    async def create(self, data: BaseModel):
        try:
            result = await self.session.execute(
                insert(self.model).values(**data.model_dump()).returning(self.model)
            )
            return self.schema.model_validate(result.scalar_one(), from_attributes=True)
        except IntegrityError as exc:
            if getattr(exc.orig, "sqlstate", None) == "23505":
                raise UniqueError
    
    async def create_bulk(self,data : list[BaseModel]):
            stmt = insert(self.model).values([model.model_dump() for model in data]).returning(self.model)
            result = await self.session.execute(stmt)
            return [self.schema.model_validate(model,from_attributes=True) for model in result.scalars().all()]

    async def delete_by_id(self, id: int):
        try:
            result = await self.session.execute(
                delete(self.model).where(self.model.id == id).returning(self.model)
            )
            return self.schema.model_validate(result.scalar_one(), from_attributes=True)
        except NoResultFound:
            raise NoFound