from src.service.base import BaseService
from src.schemas.service import ServiceCreateSchemas,ServiceRelationSchema
from src.models.enum import CategoryEnum
from src.utils.exceptions import NoFound,IdSpecializationNoFound,ServiceNoFound

class ServService(BaseService):

    async def create(self,specialization_id :int,data : ServiceCreateSchemas):
        try: 
            await self.db.master_specialization.get_object(id = specialization_id)
            new_service = await self.db.service.create(data)
            new_service_relation = await self.db.service_relation.create(ServiceRelationSchema(service_id=new_service.id,
                                                                                       masterspecialization_id=specialization_id))
            return {'new_service' : new_service, "new_service_relation" : new_service_relation}
        except NoFound:
            raise IdSpecializationNoFound
        
    async def get_all_service(self):
        return await self.db.service.get_all()
    

    async def get_all_service_by_category(self, category : CategoryEnum):
        result =  await self.db.service.get_all_by_filters(category = category)
        if result:
            return result
        else:
            raise NoFound
    
    async def delete_service(self,id : int):
        try:
            return await self.db.service.delete_by_id(id)
        except NoFound:
            raise ServiceNoFound
        