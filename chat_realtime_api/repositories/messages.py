from dataclasses import dataclass
from uuid import UUID


@dataclass
class MessageRepoInput:
    room_id: UUID
    content: str
    user_id: UUID


@dataclass
class MessageRepoOutput:
    id: UUID
    room_id: UUID
    user_id: UUID
    content: str
    timestamp: str


@dataclass
class HistoryRepoOutput:
    room_id: UUID
    messages: list[MessageRepoOutput]
    current_page: int
    page_size: int
    total_pages: int
    total_messages: int


class MessageRepository:
    def save(self, msg_input: MessageRepoInput) -> MessageRepoOutput:
        raise NotImplementedError

    def get_history_by_room_id(
        self, room_id: UUID, page: int, size: int
    ) -> HistoryRepoOutput:
        raise NotImplementedError