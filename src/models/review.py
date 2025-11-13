from sqlalchemy import String,Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from database import Base


class ReviewModel(Base):
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    id_master : Mapped[int] = mapped_column(Integer,ForeignKey("master.id",ondelete="CASCADE"))
    id_user : Mapped[int] = mapped_column(Integer,ForeignKey("users.id",ondelete="CASCADE"))
    rating : Mapped[int]
    comment : Mapped[str | None]