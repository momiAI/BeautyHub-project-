from pathlib import Path

from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    REFRESH_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    ADMIN_PHONE: str
    ADMIN_PASSWORD: str

    BASE_IDR : Path = Path(__file__).parent.parent
    FACE_IMAGE_DIR : Path = BASE_IDR / 'static' / 'face_images'
    FACE_IMAGE_DIR_BD : str = '/static/face_images/'
    PORTFOLIO_IMAGE_DIR : Path = BASE_IDR / 'static' / 'portfolio_images'
    PORTFOLIO_IMAGE_DIR_BD : str = '/static/portfolio_images/'

    FACE_IMAGE_MASTER_DIR : Path = BASE_IDR / 'static' / 'masters' / 'front_images' 
    FACE_IMAGE_MASTER_DEFAULT : Path = FACE_IMAGE_MASTER_DIR / 'no_image.png'
    FACE_IMAGE_DEFAULT_DB : str = 'static/masters/front_images/no_image.png'
    
    IMAGE_FORMAT : list = ['png', 'jpg', 'jpeg']

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
