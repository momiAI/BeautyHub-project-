from src.service.base import BaseService
from src.schemas.salons import SalonAddSchema,SalonUpdateSchema
from src.utils.exceptions import ImageInDbNoFound, IncorectTypeFile,IncorectTypeImage,SalonNoFound,NoFound,ImageInDirNoFound
from src.utils.file_utils import FilesUtils

class SalonService(BaseService):
    


    async def get_salon_by_id(self,id_salon : int):
        try:
            return await self.db.salon.get_object(id = id_salon)
        except NoFound:
            raise SalonNoFound


    async def get_salons(self,city : str | None):
        if city: 
            return await self.db.salon.get_all_by_filters(city=city)
        else:
            return await self.db.salon.get_all()


    async def salon_create(self, name : str, city : str, image, address : str):
        try:
            salon = await self.db.salon.create(SalonAddSchema(name=name,city=city,address=address))
            files_utils = FilesUtils(salon.id,salon.city)
            image_path_for_db = files_utils.save_face_image(image=image)
            data_update_path = SalonUpdateSchema(image_url=image_path_for_db)
            return await self.db.salon.update(salon.id,data_update_path)
        except IncorectTypeFile:
            raise IncorectTypeImage
        
    async def salon_update(
                        self,
                        id_salon : int, 
                        image, 
                        name : str | None = None, 
                        address : str | None = None,
                        city : str | None = None, 
                        portfolio_image : list | None = None,
                        delete_portfolio_images : list[str] | None = None
                        ):
        try:
            portfolio_image = portfolio_image or []
            delete_portfolio_images = delete_portfolio_images or []
            update_data = {}
            salon = await self.db.salon.get_object(id = id_salon)
            files_utils = FilesUtils(salon.id,salon.city)
            if image:
                if salon.image_url is None:
                    image_path_for_db = files_utils.save_face_image(image=image)
                    update_data['image_url'] = image_path_for_db
                else:
                    files_utils.update_face_image(salon.image_url, image)
            if delete_portfolio_images:
                update_data['portfolio_url'] = files_utils.delete_portfolio_images(delete_portfolio_images,salon.portfolio_url)
            if portfolio_image:
                if salon.portfolio_url is None:
                    update_data['portfolio_url'] = files_utils.save_portfolio_images(list_images = portfolio_image)
                else:
                    add_list_images_to_db = files_utils.update_portfolio_images(
                                                                                id_salon=salon.id,
                                                                                list_images_in_db=salon.portfolio_url,
                                                                                add_list_images=portfolio_image,
                                                                            )
                    update_data['portfolio_url'] = add_list_images_to_db
            if name:
                update_data['name'] = name
            if address:
                update_data['address'] = address
            if city:
                update_data['city'] = city
            return await self.db.salon.update(salon.id,SalonUpdateSchema(**update_data))

        except IncorectTypeFile:
            raise IncorectTypeFile
        except ImageInDbNoFound:
            raise ImageInDbNoFound
        except ImageInDirNoFound:
            raise ImageInDirNoFound
        except NoFound:
            raise SalonNoFound