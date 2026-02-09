import shutil
import os
from fastapi import UploadFile


from src.config import settings
from src.utils.exceptions import IncorectTypeFile,TooManyFiles,DirNoFound

class FilesUtils:

    def max_count_images(self,id_salon : int, city : str):
        name_dir = f'{id_salon}_{city}'
        images_dir = settings.PORTFOLIO_IMAGE_DIR / name_dir
        images_in_dir = list(images_dir.iterdir())
        return max([int(image.name.split('_')[0]) for image in images_in_dir])


    def delete_portfolio_images(self, id_salon : int, city : str, list_images : list[str]):
        deleted_path_images = []
        name_dir = f'{id_salon}_{city}'
        images_dir = settings.PORTFOLIO_IMAGE_DIR / name_dir
        if not os.path.exists(images_dir):
            raise DirNoFound
        images_in_dir = list(images_dir.iterdir())
        images_for_delete = [image_delete.split('/')[-1] for image_delete in list_images]
        for image in images_in_dir:
            image_path = images_dir / image.name
            if image_path.exists() and image_path.is_file() and image.name in images_for_delete:
                deleted_path_images.append(f'{settings.PORTFOLIO_IMAGE_DIR_BD}{name_dir}/{image.name}')
                image_path.unlink()
        return deleted_path_images
                

    def save_portfolio_images(self, list_images : list[UploadFile], city : str, id_salon : int, number : int | None = None):
        list_images_path_for_db = []
        count = 0 or number
        for image in list_images:
            if image.filename.split('.')[-1] not in settings.IMAGE_FORMAT:
                raise IncorectTypeFile
            
        for image in list_images:
            name_image = f"{count}_{id_salon}_{city}.{image.filename.split('.')[-1]}"
            name_dir = f'{id_salon}_{city}'
            image_path_dir = settings.PORTFOLIO_IMAGE_DIR / name_dir
            image_path = image_path_dir / name_image
            image_path_dir.mkdir(parents=True,exist_ok=True)
            with open(image_path,'wb') as buffer:
                shutil.copyfileobj(image.file,buffer)
            list_images_path_for_db.append(f'{settings.PORTFOLIO_IMAGE_DIR_BD}{name_dir}/{name_image}')
            count += 1

        return list_images_path_for_db
    
    def update_portfolio_images(self,id_salon : int, city : str, 
                                list_images_in_db : list[str],
                                add_list_images : list[UploadFile] = [], 
                                delete_portfolio_images : list[str] = [], 
                                ):
        if len(list_images_in_db) + len(add_list_images) - len(delete_portfolio_images) > 10:
            raise TooManyFiles
        if delete_portfolio_images:
            delete_list_images_to_db = self.delete_portfolio_images(id_salon,city,delete_portfolio_images)
        elif add_list_images:
            max_count = self.max_count_images(id_salon,city)
            add_list_images_to_db = self.save_portfolio_images(add_list_images,city,id_salon,max_count)
        else:
            return 'Фотографии портфолио не получены'
        
        return add_list_images_to_db,delete_list_images_to_db
        

    
   
    #4. Сохранить файлы и добавит в переменные которые вернуться.

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