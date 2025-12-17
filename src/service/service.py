from src.service.base import BaseService
from src.schemas.service import ServiceCreateSchemas

class ServService(BaseService):

    async def create(self,data : ServiceCreateSchemas):
        return await self.db.service.create(data)
    