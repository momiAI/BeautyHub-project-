from datetime import datetime
from sqlalchemy import String,Integer,ForeignKey,DateTime
from sqlalchemy.orm import Mapped,mapped_column

from src.database import Base
from src.models.enum import UserRoleEnum

class AdminModel(Base):
    __tablename__ = 'admin'

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    login : Mapped[str] = mapped_column(String(30))
    hashed_password : Mapped[str]
    role : Mapped[str] = mapped_column(default=UserRoleEnum.ADMIN.value)
    hashed_secret_word : Mapped[str]

class AdminVerifyModel(Base):
    __tablename__ = 'admin_verify'

    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    admin_id = mapped_column(Integer,ForeignKey('admin.id', ondelete = 'CASCADE'), nullable=False)
    verify_token : Mapped[str]
    expire_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=True)
    attempts : Mapped[int] = mapped_column(default=0)
    last_attempt : Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=True)