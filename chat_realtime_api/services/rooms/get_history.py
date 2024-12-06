from dataclasses import dataclass
from uuid import UUID

from chat_realtime_api.repositories.messages import (
    MessageRepository,
)
from chat_realtime_api.repositories.rooms import RoomRepository
from chat_realtime_api.services.errors.exceptions import RoomNotFoundException


@dataclass
class MessageOutput:
    id: str
    room_id: str
    user_id: str
    content: str
    timestamp: str


@dataclass
class GetHistoryOutput:
    room_id: str
    messages: list[MessageOutput]
    current_page: int
    page_size: int
    total_pages: int
    total_messages: int


class GetHistoryService:
    def __init__(self, msg_repo: MessageRepository, room_repo: RoomRepository):
        self.msg_repo = msg_repo
        self.room_repo = room_repo

    def execute(self, room_id: UUID, page: int, size: int) -> GetHistoryOutput:
        if not self.room_repo.room_exists(room_id):
            raise RoomNotFoundException(room_id)

        room_output = self.msg_repo.get_history_by_room_id(
            room_id=room_id, page=page, size=size
        )

        return GetHistoryOutput(
            room_id=room_output.room_id,
            messages=room_output.messages,
            current_page=room_output.current_page,
            page_size=room_output.page_size,
            total_pages=room_output.total_pages,
            total_messages=room_output.total_messages,
        )
