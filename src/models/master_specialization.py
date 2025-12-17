from sqlalchemy import Integer,String
from sqlalchemy.orm import Mapped,mapped_column,relationship

from src.database import Base


class MasterSpecializationModel(Base):
    __tablename__ = "masterspecialization"

    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    name : Mapped[str] = mapped_column(String(50))

    master : Mapped[list["MasterModel"]] = relationship(secondary="specialization_master", back_populates="specialization") # noqa: F821 # type: ignore
    service : Mapped[list["ServiceModel"]] = relationship(secondary="specialization_service", back_populates="masterspecialization") # noqa: F821 # type: ignore