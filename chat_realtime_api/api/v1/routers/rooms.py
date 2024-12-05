from http import HTTPStatus
from typing import Dict
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from chat_realtime_api.api.v1.errors.error_handlers import handle_error
from chat_realtime_api.api.v1.schemas.history import HistorySchema
from chat_realtime_api.api.v1.schemas.rooms import (
    ListRoomOutputSchema,
    RoomInputSchema,
    RoomOutputSchema,
)
from chat_realtime_api.infra.config.security import get_current_user
from chat_realtime_api.infra.db.session import get_session
from chat_realtime_api.infra.sqlalchemy_repositories.rooms import (
    SqlAlchemyRoomRepository,
)
from chat_realtime_api.services.rooms.create import (
    CreateRoomInput,
    CreateRoomService,
)
from chat_realtime_api.services.rooms.get import GetRoomService

router = APIRouter(prefix='/api/v1', tags=['rooms'])


@router.post(
    '/rooms',
    status_code=HTTPStatus.CREATED,
    response_model=RoomOutputSchema,
)
def create_room(
    room_schema: RoomInputSchema,
    session: Session = Depends(get_session),
    _: Dict = Depends(get_current_user),
):
    repo = SqlAlchemyRoomRepository(session)
    service = CreateRoomService(repo)
    try:
        room = service.execute(
            CreateRoomInput(
                name=room_schema.name,
                description=room_schema.description,
            )
        )

        return RoomOutputSchema(
            id=room.id,
            name=room.name,
            description=room.description,
        )
    except Exception as e:
        print(e)
        raise handle_error(e)


@router.get(
    '/rooms',
    status_code=HTTPStatus.OK,
    response_model=ListRoomOutputSchema,
)
def list_rooms(
    session: Session = Depends(get_session),
    _: Dict = Depends(get_current_user),
):
    repo = SqlAlchemyRoomRepository(session)
    service = GetRoomService(repo)
    try:
        rooms = service.execute()

        return ListRoomOutputSchema(
            rooms=[
                RoomOutputSchema(
                    id=room.id,
                    name=room.name,
                    description=room.description,
                )
                for room in rooms
            ]
        )
    except Exception as e:
        print(e)
        raise handle_error(e)


@router.get(
    '/rooms/{room_id}/history/',
    status_code=HTTPStatus.OK,
    response_model=HistorySchema,
)
def get_room_history(
    room_id: UUID,
    session: Session = Depends(get_session),
    _: Dict = Depends(get_current_user),
):
    try:
        pass
    except Exception as e:
        print(e)
        raise handle_error(e)
