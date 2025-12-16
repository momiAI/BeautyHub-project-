from datetime import datetime
from sqlalchemy import Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from src.models.enum import ReceptionStatusEnum


class ReceptionModel(Base):
    __tablename__ = "reception"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_user: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    id_master: Mapped[int] = mapped_column(Integer, ForeignKey("master.id"))
    id_service: Mapped[int] = mapped_column(Integer, ForeignKey("service.id"))
    date_time: Mapped[datetime]
    status: Mapped[str] = mapped_column(Enum(ReceptionStatusEnum, native_enum=False))
