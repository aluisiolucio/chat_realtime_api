from contextlib import asynccontextmanager
from uuid import UUID

import anyio
from broadcaster import Broadcast
from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketException,
)
from sqlalchemy.orm import Session

from chat_realtime_api.infra.config.settings import Settings
from chat_realtime_api.infra.db.session import get_session
from chat_realtime_api.infra.sqlalchemy_repositories.rooms import (
    SqlAlchemyRoomRepository,
)


async def chatroom_ws_receiver(websocket: WebSocket, channel: str):
    async for message in websocket.iter_text():
        await broadcast.publish(channel=channel, message=message)


async def chatroom_ws_sender(websocket: WebSocket, channel: str):
    async with broadcast.subscribe(channel=channel) as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)


broadcast = Broadcast(Settings().DATABASE_URL)


@asynccontextmanager
async def lifespan(app):
    await broadcast.connect()
    try:
        yield
    finally:
        await broadcast.disconnect()


router = APIRouter(prefix='/api/v1', tags=['chat'], lifespan=lifespan)


@router.websocket('/chat/{room_id}')
async def chat_websocket(
    websocket: WebSocket,
    room_id: UUID,
    session: Session = Depends(get_session),
):
    repo = SqlAlchemyRoomRepository(session)

    if not repo.room_exists(room_id):
        raise WebSocketException(code=404, reason='Room not found')

    room_id_str = str(room_id)
    await websocket.accept()

    async with anyio.create_task_group() as task_group:

        async def run_chatroom_ws_receiver() -> None:
            await chatroom_ws_receiver(websocket, room_id_str)
            task_group.cancel_scope.cancel()

        task_group.start_soon(run_chatroom_ws_receiver)
        await chatroom_ws_sender(websocket, room_id_str)
