from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from chat_realtime_api.infra.models.rooms import RoomModel
from chat_realtime_api.repositories.rooms import (
    RoomRepoInput,
    RoomRepoOutput,
    RoomRepository,
)


class SqlAlchemyRoomRepository(RoomRepository):
    def __init__(self, session: Session):
        self._session = session

    def save(self, room_input: RoomRepoInput) -> RoomRepoOutput | str:
        room_db = self._session.scalar(
            select(RoomModel).where(RoomModel.name == room_input.name)
        )

        if room_db:
            return 'Room already exists'

        room_db = RoomModel(
            id=uuid4(),
            name=room_input.name,
            description=room_input.description,
        )

        self._session.add(room_db)
        self._session.commit()
        self._session.refresh(room_db)

        return RoomRepoOutput(
            id=room_db.id,
            name=room_db.name,
            description=room_db.description,
        )

    def get_all(self) -> list[RoomRepoOutput]:
        rooms_db = self._session.scalars(select(RoomModel)).all()

        if not rooms_db:
            return []

        return [
            RoomRepoOutput(
                id=room_db.id,
                name=room_db.name,
                description=room_db.description,
            )
            for room_db in rooms_db
        ]
