from dataclasses import dataclass
from uuid import UUID


@dataclass
class RoomRepoInput:
    name: str
    creator_id: UUID
    description: str | None = None


@dataclass
class RoomRepoOutput:
    id: UUID
    name: str
    creator_id: UUID
    description: str | None = None


class RoomRepository:
    def save(self, room_input: RoomRepoInput) -> RoomRepoOutput | str:
        raise NotImplementedError

    def get_all(self) -> list[RoomRepoOutput]:
        raise NotImplementedError

    def room_exists(self, room_id: UUID) -> bool:
        raise NotImplementedError
