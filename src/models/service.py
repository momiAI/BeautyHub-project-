from sqlalchemy import Integer, String, Enum,Table,Column,ForeignKey,UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.database import Base
from src.models.enum import CategoryEnum


class ServiceModel(Base):
    __tablename__ = "service"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(Enum(CategoryEnum, native_enum=False))
    masterspecialization : Mapped[list["MasterSpecializationModel"]] = relationship(secondary="specialization_service", back_populates="service") # noqa: F821 # type: ignore

    masters : Mapped[list["MasterServiceModel"]] = relationship(back_populates="service") 

class MasterServiceModel(Base):
    __tablename__ = "MasterServiceUnique"
    id : Mapped[int] = mapped_column(Integer, primary_key= True)
    id_master : Mapped[int] = mapped_column(Integer, ForeignKey("master.id"), nullable= False)
    id_service : Mapped[int] = mapped_column(Integer, ForeignKey("service.id"), nullable=False)
    duration_minutes : Mapped[int]
    price : Mapped[int]

    master : Mapped["MasterModel"] = relationship(back_populates="services") # noqa: F821 # type: ignore

    service : Mapped["ServiceModel"] = relationship(back_populates="masters")

    __table_args__ = (UniqueConstraint("id_master","id_service"),)


specialization_service = Table(
        "specialization_service",
        Base.metadata,
        Column("service_id", ForeignKey("service.id", ondelete="CASCADE"), primary_key=True),
        Column("masterspecialization_id", ForeignKey("masterspecialization.id", ondelete="CASCADE"), primary_key=True),
    )