from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from chat_realtime_api.infra.models.base import table_registry


@table_registry.mapped_as_dataclass
class RoomModel:
    __tablename__ = 'rooms'

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)

    creator_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )
