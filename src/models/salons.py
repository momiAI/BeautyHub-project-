from sqlalchemy import Integer,String
from sqlalchemy.orm import Mapped,mapped_column

from src.database import Base



class SalonModel(Base):
    __tablename__ = 'salons'

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String(50))
    city : Mapped[str] = mapped_column(String(30))
    address : Mapped[str] = mapped_column(String(100)) 
    image_url : Mapped[str | None]