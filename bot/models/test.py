from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.question import Question


class Test(Base):

    __tablename__ = "tests"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        unique=True
    )
    name: Mapped[str] = mapped_column(
        String(),
        unique=True,
    )
    questions: Mapped[list["Question"]] = relationship(
        back_populates="test",
        cascade="all, delete"
    )