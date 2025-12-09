from sqlalchemy import Integer,String,CheckConstraint,Enum
from sqlalchemy.orm import mapped_column,Mapped,relationship
from src.database import Base
from src.models.enum import CategoryEnum


class ServiceModel(Base):
    __tablename__ = 'service'

    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    name : Mapped[str] = mapped_column(String(100))
    price : Mapped[int]
    duration_minutes : Mapped[int] 
    category : Mapped[str] = mapped_column(Enum(CategoryEnum,native_enum=False))

    masters : Mapped[list["MasterModel"]] = relationship(secondary="specialization_master",back_populates="specialization") # type: ignore 

