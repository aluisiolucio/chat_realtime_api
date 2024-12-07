from http import HTTPStatus
from typing import Annotated, Dict
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from chat_realtime_api.api.v1.errors.error_handlers import handle_error
from chat_realtime_api.api.v1.schemas.history import (
    HistorySchema,
    MessageSchema,
    PaginationQuerySchema,
    PaginationSchema,
    UserSchema,
)
from chat_realtime_api.api.v1.schemas.rooms import (
    ListRoomOutputSchema,
    RoomInputSchema,
    RoomOutputSchema,
)
from chat_realtime_api.infra.config.security import get_current_user
from chat_realtime_api.infra.db.session import get_session
from chat_realtime_api.infra.sqlalchemy_repositories.messages import (
    SqlAlchemyMessageRepository,
)
from chat_realtime_api.infra.sqlalchemy_repositories.rooms import (
    SqlAlchemyRoomRepository,
)
from chat_realtime_api.services.rooms.create import (
    CreateRoomInput,
    CreateRoomService,
)
from chat_realtime_api.services.rooms.get import GetRoomService
from chat_realtime_api.services.rooms.get_history import GetHistoryService

router = APIRouter(prefix='/api/v1', tags=['rooms'])


@router.post(
    '/rooms',
    status_code=HTTPStatus.CREATED,
    response_model=RoomOutputSchema,
)
def create_room(
    room_schema: RoomInputSchema,
    session: Session = Depends(get_session),
    current_user: Dict = Depends(get_current_user),
):
    repo = SqlAlchemyRoomRepository(session)
    service = CreateRoomService(repo)
    try:
        room = service.execute(
            CreateRoomInput(
                name=room_schema.name,
                creator_id=UUID(current_user['uid']),
                description=room_schema.description,
            )
        )

        return RoomOutputSchema(
            id=room.id,
            name=room.name,
            creator_id=room.creator_id,
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
                    creator_id=room.creator_id,
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
    pagination_query_schema: Annotated[PaginationQuerySchema, Query()],
    room_id: UUID,
    session: Session = Depends(get_session),
    _: Dict = Depends(get_current_user),
):
    msg_repo = SqlAlchemyMessageRepository(session)
    room_repo = SqlAlchemyRoomRepository(session)

    service = GetHistoryService(msg_repo, room_repo)
    try:
        history = service.execute(
            room_id=room_id,
            page=pagination_query_schema.page,
            size=pagination_query_schema.size,
        )

        return HistorySchema(
            room_id=room_id,
            messages=[
                MessageSchema(
                    id=msg.id,
                    room_id=msg.room_id,
                    user=UserSchema(
                        id=msg.user.id,
                        name=msg.user.name,
                    ),
                    content=msg.content,
                    timestamp=msg.timestamp,
                )
                for msg in history.messages
            ],
            pagination=PaginationSchema(
                current_page=history.current_page,
                page_size=history.page_size,
                total_pages=history.total_pages,
                total_messages=history.total_messages,
            ),
        )
    except Exception as e:
        print(e)
        raise handle_error(e)
