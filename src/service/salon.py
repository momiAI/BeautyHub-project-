from src.service.base import BaseService
from src.schemas.salons import SalonAddSchema


class SalonService(BaseService):

    async def salon_create(self, name : str, city : str, image):
        return image.filename
        #дописать сохранение файла