from datetime import time, date, datetime
from sqlalchemy import (
    Integer,
    ForeignKey,
    Text,
    Time,
    Date,
    Table,
    Column,
    Enum,
    UniqueConstraint,
    String,
    ARRAY,
    DateTime,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base
from src.models.enum import WeekDayEnum, MasterRequestStatusEnum


class MasterModel(Base):
    __tablename__ = "master"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_user: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    bio: Mapped[str] = mapped_column(Text())

    specialization: Mapped[list["MasterSpecializationModel"]] = relationship( # noqa: F821 # type: ignore
        secondary="specialization_master", back_populates="master"
    )  
    work_days: Mapped[list["WorkDayModel"]] = relationship(
        back_populates="master", cascade="all, delete-orphan"
    )
    day_offs: Mapped[list["DayOffModel"]] = relationship(
        back_populates="master", cascade="all, delete-orphan"
    )

    services : Mapped[list["MasterServiceModel"]] = relationship(back_populates="master")# noqa: F821 # type: ignore

master_specialization_table = Table(
    "specialization_master",
    Base.metadata,
    Column("master_id", ForeignKey("master.id", ondelete="CASCADE"), primary_key=True),
    Column("masterspecialization_id", ForeignKey("masterspecialization.id", ondelete="CASCADE"), primary_key=True),
)


class WorkDayModel(Base):
    __tablename__ = "timetable"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_master: Mapped[int] = mapped_column(
        Integer, ForeignKey("master.id", ondelete="CASCADE")
    )
    day_of_week: Mapped[list[WeekDayEnum]] = mapped_column(
        ARRAY(Enum(WeekDayEnum, 
        length = 15,
        native_enum=False))
    )
    start_time: Mapped[time] = mapped_column(Time())
    end_time: Mapped[time] = mapped_column(Time())

    master: Mapped["MasterModel"] = relationship(back_populates="work_days")

    __table_args__ = (
        UniqueConstraint("id_master", "day_of_week", name="uq_master_day"),
    )


class DayOffModel(Base):
    __tablename__ = "dayoff"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_master: Mapped[int] = mapped_column(
        Integer, ForeignKey("master.id", ondelete="CASCADE")
    )
    day: Mapped[date] = mapped_column(Date)
    reason: Mapped[str | None]

    master: Mapped["MasterModel"] = relationship(back_populates="day_offs")


class MasterRequestModel(Base):
    __tablename__ = "masterrequest"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_user: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    bio_short: Mapped[str] = mapped_column(String(50))
    specializations: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    portfolio: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    status: Mapped[MasterRequestStatusEnum] = mapped_column(
        Enum(MasterRequestStatusEnum, native_enum=False)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
