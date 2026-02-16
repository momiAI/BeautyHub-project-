from sqlalchemy import Column, ForeignKey, Integer,String,ARRAY, Table
from sqlalchemy.orm import Mapped,mapped_column,relationship

from src.database import Base



class SalonModel(Base):
    __tablename__ = 'salons'

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String(50))
    city : Mapped[str] = mapped_column(String(30))
    address : Mapped[str] = mapped_column(String(100)) 
    image_url : Mapped[str | None]
    portfolio_url : Mapped[list['str'] | None] = mapped_column(ARRAY(String),nullable=True)
    
    masters : Mapped[list['MasterModel']] = relationship( # noqa: F821 # type: ignore
        secondary='master_salon',
        back_populates='salons'
    )

master_salon = Table(
    'master_salon',
    Base.metadata,
    Column('id_master',ForeignKey('master.id', ondelete='CASCADE'), primary_key=True),
    Column('id_salon',ForeignKey('salons.id', ondelete='CASCADE'), primary_key=True )
)