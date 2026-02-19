import shutil
import os
from fastapi import UploadFile
from typing import NamedTuple

from src.config import settings
from src.utils.exceptions import IncorectTypeFile,TooManyFiles,DirNoFound,ImageInDbNoFound,ImageInDirNoFound

class ImagePathName(NamedTuple):
    name : str
    path : str

class FilesUtils:

    def __init__(self,id_salon,city):
        self.id_salon = id_salon
        self.city = city
        self.name_dir = f'{self.id_salon}_{self.city}'
        self.path_in_portfolio_dir = settings.PORTFOLIO_IMAGE_DIR / self.name_dir
        self.path_portfolio_to_db = f'{settings.PORTFOLIO_IMAGE_DIR_BD}{self.name_dir}'


    def max_count_images(self) -> list[int]:
        if not self.path_in_portfolio_dir.exists():
            self.path_in_portfolio_dir.mkdir(parents=True, exist_ok=True)
        images_in_dir = list(self.path_in_portfolio_dir.iterdir())
        list_count = sorted([int(image.name.split('_')[0]) for image in images_in_dir])
        free_count = sorted([free for free in range(10) if free not in list_count])
        return free_count

    def _check_images_in_db_and_path(self, list_images : list[str], list_images_in_db : list[str]):
        for images_url in list_images:
                if images_url not in list_images_in_db:
                    raise ImageInDbNoFound
        if not os.path.exists(self.path_in_portfolio_dir):
            raise DirNoFound

    def delete_portfolio_images(self,list_images : list[str], list_images_in_db : list[str]) -> list[str]:
        list_images_in_db = list_images_in_db or []
        self._check_images_in_db_and_path(list_images,list_images_in_db)
        deleted_path_images = []
        images_in_dir = [image.name for image in self.path_in_portfolio_dir.iterdir() if image.is_file()]
        images_for_delete = [image_delete.split('/')[-1] for image_delete in list_images]
        for image_name  in images_for_delete:
            if image_name not in images_in_dir:
                raise ImageInDirNoFound
        for image in images_in_dir:
            image_path = self.path_in_portfolio_dir / image
            if image_path.exists() and image_path.is_file() and image in images_for_delete:
                deleted_path_images.append(f'{self.path_portfolio_to_db}/{image}')
                image_path.unlink()
        return deleted_path_images
                

    def _check_format_files(self, list_images : list[UploadFile]):
        for image in list_images:
            if image.filename.split('.')[-1] not in settings.IMAGE_FORMAT:
                raise IncorectTypeFile
    

    def _saves_portfolio_images(self, list_images : list[UploadFile]):
        count = 0
        list_count = self.max_count_images()
        if len(list_count) < len(list_images):
            raise TooManyFiles
        for image in list_images:
            name_image = f"{list_count[count]}_{self.id_salon}_{self.city}.{image.filename.split('.')[-1]}"
            image_path = self.path_in_portfolio_dir / name_image
            with open(image_path,'wb') as buffer:
                shutil.copyfileobj(image.file,buffer)
            count += 1


    def save_portfolio_images(self, list_images : list[UploadFile]) -> list[str]:
        self._check_format_files(list_images)
        self._saves_portfolio_images(list_images)
        images_in_dir = list(self.path_in_portfolio_dir.iterdir())
        list_images_path_for_db = [f'{self.path_portfolio_to_db}/{name.name}' for name in images_in_dir]
        return list_images_path_for_db
    

    def update_portfolio_images(self,
                                id_salon : int,
                                list_images_in_db : list[str],
                                add_list_images : list[UploadFile] = [], 
                                ) -> list[str]:
        if len(list_images_in_db) + len(add_list_images) > 10:
            raise TooManyFiles
        if add_list_images:
            add_list_images_to_db = self.save_portfolio_images(add_list_images)
        else:
            add_list_images_to_db = []
        return add_list_images_to_db
        

    def _get_face_image_path(self, image : UploadFile) -> ImagePathName:
        format_image = image.filename.split('.')[-1]
        if format_image not in settings.IMAGE_FORMAT:
            raise IncorectTypeFile
        name_image = f"{self.name_dir}_FACE.{format_image}"
        path_image = settings.FACE_IMAGE_DIR / name_image
        return ImagePathName(name_image,path_image)


    def save_face_image(self, image : UploadFile) -> str:
        path_name = self._get_face_image_path(image)
        with open(path_name.path,'wb') as buffer:
            shutil.copyfileobj(image.file,buffer)
        return f'{settings.FACE_IMAGE_DIR_BD}{path_name.name}'

    def update_face_image(self,image_url : str, new_image : UploadFile):
        path_to_file = settings.FACE_IMAGE_DIR / image_url.split('/')[-1]
        with open(path_to_file, 'wb') as buffer:
            shutil.copyfileobj(new_image.file,buffer)
