from datetime import time,date
from sqlalchemy import Integer,String, ForeignKey,Text,Time,Date
from sqlalchemy.orm import mapped_column,Mapped,relationship
from src.database import Base



class MasterModel(Base):
    __tablename__ = 'master'
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    id_user : Mapped[int] = mapped_column(Integer,ForeignKey("users.id"), nullable= False)
    bio : Mapped[str] = mapped_column(Text())

    specialization : Mapped[list["SpecializationModel"]] = relationship(secondary="specialization_master", back_populates="masters") #type: ignore
    work_days : Mapped[list["WorkDayModel"]] = relationship(back_populates="master",cascade="all, delete-orphan")
    day_offs : Mapped[list["DayOffModel"]] = relationship(back_populates="master", cascade="all, delete-orphan")


class SpecializationModel(Base):
    __tablename__ = "specialization_master"

    id_master : Mapped[int] = mapped_column(Integer,ForeignKey("master.id", ondelete="CASCADE"), primary_key= True)
    id_service : Mapped[int] = mapped_column(Integer, ForeignKey("service.id", ondelete="CASCADE"))


class WorkDayModel(Base):
    __tablename__ = "timetable"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    id_master : Mapped[int] = mapped_column(Integer, ForeignKey("master.id",ondelete="CASCADE"))
    day_of_week: Mapped[str] = mapped_column(String(10))  
    start_time: Mapped[time] = mapped_column(Time())  
    end_time: Mapped[time] = mapped_column(Time())   

    master : Mapped["MasterModel"] = relationship(back_populates="work_days")


class DayOffModel(Base):
    __tablename__ = "dayoff"

    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    id_master : Mapped[int] = mapped_column(Integer,ForeignKey("master.id", ondelete="CASCADE"))
    day : Mapped[date] = mapped_column(Date)
    reason : Mapped[str | None]

    master : Mapped["MasterModel"] = relationship(back_populates="day_offs")