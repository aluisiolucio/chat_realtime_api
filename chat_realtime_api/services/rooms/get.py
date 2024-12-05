from chat_realtime_api.repositories.rooms import (
    RoomRepoOutput,
    RoomRepository,
)


class GetRoomService:
    def __init__(self, repository: RoomRepository):
        self.repository = repository

    def execute(self) -> list[RoomRepoOutput]:
        room_output = self.repository.get_all()

        return room_output
