from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from chat_realtime_api.repositories.messages import (
    MessageRepoInput,
    MessageRepository,
)
from chat_realtime_api.repositories.rooms import RoomRepository
from chat_realtime_api.services.errors.exceptions import RoomNotFoundException


@dataclass
class CreateMessageInput:
    room_id: UUID
    content: str
    user_id: UUID


@dataclass
class CreateMessageOutput:
    id: UUID
    room_id: UUID
    user_id: UUID
    content: str
    timestamp: datetime


class CreateMessageService:
    def __init__(self, msg_repo: MessageRepository, room_repo: RoomRepository):
        self.msg_repo = msg_repo
        self.room_repo = room_repo

    def execute(self, input: CreateMessageInput) -> CreateMessageOutput:
        if not self.room_repo.room_exists(input.room_id):
            raise RoomNotFoundException(input.room_id)

        room_output = self.msg_repo.save(
            MessageRepoInput(
                room_id=input.room_id,
                content=input.content,
                user_id=input.user_id,
            )
        )

        return CreateMessageOutput(
            id=room_output.id,
            room_id=room_output.room_id,
            user_id=room_output.user.id,
            content=room_output.content,
            timestamp=room_output.timestamp,
        )
