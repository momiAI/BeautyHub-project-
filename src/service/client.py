from datetime import datetime

from src.service.base import BaseService
from src.utils.exceptions import ClientUniqueError
from src.schemas.client import ClientDbSchema
from src.service.reception import RecepionService
from src.schemas.reception import ReceptionRequestSchema

class ClientService(BaseService):

    async def get_client(self,phone : str):
        return await self.db.client.get_object_or_none(phone = phone)

    
    async def create_client(self,phone : str, id_user : int | None = None):

        client = await self.get_client(phone)
        if client:
            raise ClientUniqueError
        if id_user is None:
            return await self.db.client.create(ClientDbSchema(phone = phone, is_guest=True,rating=0.0, id_user = None))
        else:
            return await self.db.client.create(ClientDbSchema(phone = phone, is_guest=False,rating=0.0, id_user=id_user))


    async def record_client(self,phone : str,data :ReceptionRequestSchema):

        client = await self.get_client(phone)
        if client is None:
            client = await self.create_client(phone)

        return await RecepionService(self.db).subscribe(client.id,data)


