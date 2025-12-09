from src.database import Base
from sqlalchemy import Integer,String,Enum,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
from src.models.enum import UserRoleEnum

class UsersModel(Base):
    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    phone : Mapped[str] = mapped_column(String(20),unique=True)
    name : Mapped[str] = mapped_column(String(50))
    password_hash : Mapped[str]
    role : Mapped[str] = mapped_column(Enum(UserRoleEnum))

class UserRatingModel(Base):
    __tablename__ = "user_rating"

    id_from: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    id_to: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    rating: Mapped[int]