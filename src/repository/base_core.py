from sqlalchemy import Table,insert,select
from sqlalchemy.exc import IntegrityError

from pydantic import BaseModel
from src.utils.exceptions import NoFound

class BaseCoreRep:
    table = Table
    schema = BaseModel

    def __init__(self, session):
        self.session = session

    async def create_bulk(self,data : list[BaseModel]):
            stmt = insert(self.table).values([model.model_dump() for model in data]).returning(self.table)
            result = await self.session.execute(stmt)
            return [self.schema.model_validate(model,from_attributes=True) for model in result.mappings().all()]
    
    
    async def get_all_by_name_column_id(self, id : int, name_column : str):
            result = await self.session.execute(select(self.table).where(self.table.c[name_column] == id)) 
            return [self.schema.model_validate(model) for model in result.mappings().all()]