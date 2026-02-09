from src.service.base import BaseService
from src.schemas.salons import SalonAddSchema,SalonUpdateSchema
from src.utils.exceptions import IncorectTypeFile,IncorectTypeImage,SalonNoFound,NoFound
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
        
    async def salon_update_(
                        self,
                        id_salon : int, 
                        name : str, 
                        address : str,
                        city : str, 
                        image, 
                        portfolio_image : list,
                        delete_portfolio_images : list[str]
                        ):
        try:
            salon = await self.db.salon.get_object(id = id_salon)
            if image:
                if salon.image_url is None:
                    image_path_for_db = files_utils.save_face_image(image=image,city=salon.city,id_salon=salon.id)
                    salon = await self.db.salon.update(salon.id,SalonUpdateSchema(image_url = image_path_for_db))
                else:
                    files_utils.update_face_image(salon.image_url, image)
            elif portfolio_image:
                if salon.portfolio_url is None:
                    list_images_path_for_db = files_utils.save_portfolio_images(list_images = portfolio_image, city = salon.city, id_salon = salon.id)
                    salon = await self.db.salon.update(salon.id,SalonUpdateSchema(portfolio_url = list_images_path_for_db))
            
                    
            if name or address or city:
                data_update = SalonUpdateSchema(name=name,address=address,city=city)
                return await self.db.salon.update(id=salon.id, values=data_update)
            else:
                return 'Строковые наименования не обновлены'
        except NoFound:
            raise SalonNoFound
        except IncorectTypeFile:
            raise IncorectTypeFile