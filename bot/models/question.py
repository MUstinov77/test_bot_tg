from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Question(Base):

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        unique=True,
    )
    text: Mapped[str] = mapped_column(
        String(30)
    )
    right_answer: Mapped[str] = mapped_column(
        String()
    )
    number_of_variants: Mapped[int] = mapped_column(
        Integer(),
        default=4,
    )
    test_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tests.id",
        )
    )
    test = relationship(
        "Test",
        back_populates="questions",
        uselist=False,
    )