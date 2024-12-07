from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chat_realtime_api.infra.models.base import table_registry


@table_registry.mapped_as_dataclass
class UserModel:
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    messages: Mapped[List['MessageModel']] = relationship()  # noqa: F821 # type: ignore
