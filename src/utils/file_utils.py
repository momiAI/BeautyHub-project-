import shutil
from fastapi import UploadFile

from src.config import settings
from src.utils.exceptions import IncorectTypeFile

class FilesUtils:

    def save_face_image(self, image : UploadFile, city : str, id_salon : int):
        format_image = image.filename.split('.')[-1]
        if format_image not in settings.IMAGE_FORMAT:
            raise IncorectTypeFile
        name_image = f"{id_salon}_{city}_FACE.{format_image}"
        image_path = settings.FACE_IMAGE_DIR / name_image
        with open(image_path,'wb') as buffer:
            shutil.copyfileobj(image.file,buffer)
        return f'{settings.FACE_IMAGE_DIR_BD}{name_image}'



files_utils = FilesUtils()