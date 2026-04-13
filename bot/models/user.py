from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from core.enum import UserStatus
from models.base import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        unique=True
    )
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(
        Enum(UserStatus),
        server_default=UserStatus.common
    )

    def __str__(self):
        return f"@{self.username}"