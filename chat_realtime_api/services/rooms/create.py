from dataclasses import dataclass

from chat_realtime_api.repositories.rooms import (
    RoomRepoInput,
    RoomRepository,
)
from chat_realtime_api.services.errors.exceptions import (
    RoomAlreadyExistsException,
)


@dataclass
class CreateRoomInput:
    name: str
    description: str | None = None


@dataclass
class CreateRoomOutput:
    id: str
    name: str
    description: str | None = None


class CreateRoomService:
    def __init__(self, repository: RoomRepository):
        self.repository = repository

    def execute(self, input: CreateRoomInput) -> CreateRoomOutput:
        room_input = RoomRepoInput(
            name=input.name,
            description=input.description,
        )

        room_output = self.repository.save(room_input)

        if isinstance(room_output, str):
            raise RoomAlreadyExistsException(room_input.name)

        return CreateRoomOutput(
            id=room_output.id,
            name=room_output.name,
            description=room_output.description,
        )
