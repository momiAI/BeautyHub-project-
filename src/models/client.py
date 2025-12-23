from sqlalchemy import Integer,String,ForeignKey,Boolean,CheckConstraint,Float
from sqlalchemy.orm import Mapped,mapped_column

from src.database import Base


class ClientModel(Base):
    __tablename__ = "client"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    id_user : Mapped[int | None] = mapped_column(Integer,ForeignKey("users.id",ondelete="CASCADE"), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True)
    is_guest : Mapped[bool] = mapped_column(Boolean)
    rating : Mapped[float] = mapped_column(Float, default= 0.0)


class ClientRatingModel(Base):
    __tablename__ = "client_rating"

    id_from: Mapped[int] = mapped_column(ForeignKey("master.id"), primary_key=True)
    id_to: Mapped[int] = mapped_column(ForeignKey("client.id"), primary_key=True)
    rating: Mapped[int]

    __table_args__ = (
        CheckConstraint(
        "rating >= 1 AND rating <= 5", name = "ck_example_value_ranges_1_5"
    ),
)
