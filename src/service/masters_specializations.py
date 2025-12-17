from src.service.base import BaseService
from src.schemas.masters import MasterSpecializationCreateSchema

class MasterSpecializationService(BaseService):

    async def get_all(self):
        return await self.db.master_specialization.get_all()
    
    async def create(self, data : MasterSpecializationCreateSchema):
        return await self.db.master_specialization.create(data)