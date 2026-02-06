import shutil
from fastapi import UploadFile

from src.config import settings
from src.utils.exceptions import IncorectTypeFile

class FilesUtils:

    def save_portfolio_images(self, list_images : list[UploadFile], city : str, id_salon : int):
        list_images_path_for_db = []
        count = 0
        for image in list_images:
            if image.filename.split('.')[-1] not in settings.IMAGE_FORMAT:
                raise IncorectTypeFile
            
        for image in list_images:
            name_image = f"{count}_{id_salon}_{city}.{image.filename.split('.')[-1]}"
            image_path = settings.PORTFOLIO_IMAGE_DIR / name_image
            with open(image_path,'wb') as buffer:
                shutil.copyfileobj(image.file,buffer)
            list_images_path_for_db.append(f'{settings.PORTFOLIO_IMAGE_DIR_BD}{name_image}')
            count += 1

        return list_images_path_for_db

    def save_face_image(self, image : UploadFile, city : str, id_salon : int):
        format_image = image.filename.split('.')[-1]
        if format_image not in settings.IMAGE_FORMAT:
            raise IncorectTypeFile
        name_image = f"{id_salon}_{city}_FACE.{format_image}"
        image_path = settings.FACE_IMAGE_DIR / name_image
        with open(image_path,'wb') as buffer:
            shutil.copyfileobj(image.file,buffer)
        return f'{settings.FACE_IMAGE_DIR_BD}{name_image}'

    def update_face_image(self,image_url : str, new_image : UploadFile):
        path_to_file = settings.FACE_IMAGE_DIR / image_url.split('/')[-1]
        with open(path_to_file, 'wb') as buffer:
            shutil.copyfileobj(new_image.file,buffer)


files_utils = FilesUtils()