from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from chat_realtime_api.repositories.messages import (
    MessageRepository,
)
from chat_realtime_api.repositories.rooms import RoomRepository
from chat_realtime_api.services.errors.exceptions import RoomNotFoundException


@dataclass
class UserOutput:
    name: str


@dataclass
class GetMessageOutput:
    user: UserOutput
    content: str
    timestamp: datetime


class GetMessageService:
    def __init__(self, msg_repo: MessageRepository, room_repo: RoomRepository):
        self.msg_repo = msg_repo
        self.room_repo = room_repo

    def execute(self, room_id: UUID) -> GetMessageOutput:
        if not self.room_repo.room_exists(room_id):
            raise RoomNotFoundException(room_id)

        messages = self.msg_repo.get_messages_by_room_id(room_id=room_id)

        return [
            GetMessageOutput(
                user=UserOutput(name=msg.user.name),
                content=msg.content,
                timestamp=msg.timestamp,
            )
            for msg in messages
        ]
