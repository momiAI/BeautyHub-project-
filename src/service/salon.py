from src.service.base import BaseService
from src.schemas.salons import SalonAddSchema,SalonUpdateSchema
from src.utils.exceptions import IncorectTypeFile,IncorectTypeImage
from src.utils.file_utils import files_utils


class SalonService(BaseService):

    async def get_salons(self,city : str | None):
        if city: 
            return await self.db.salon.get_all_by_filters(city=city)
        else:
            return await self.db.salon.get_all()


    async def salon_create(self, name : str, city : str, image, address : str):
        try:
            salon = await self.db.salon.create(SalonAddSchema(name=name,city=city,address=address))
            image_path_for_db = files_utils.save_face_image(image=image,city=city, id_salon=salon.id)
            data_update_path = SalonUpdateSchema(image_url=image_path_for_db)
            return await self.db.salon.update(salon.id,data_update_path)
        except IncorectTypeFile:
            raise IncorectTypeImage