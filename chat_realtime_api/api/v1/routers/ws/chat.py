from contextlib import asynccontextmanager
from typing import Dict
from uuid import UUID

import anyio
from broadcaster import Broadcast
from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session

from chat_realtime_api.api.v1.errors.error_handlers import handle_error
from chat_realtime_api.infra.config.security import get_current_user_ws
from chat_realtime_api.infra.config.settings import Settings
from chat_realtime_api.infra.db.session import get_session
from chat_realtime_api.infra.sqlalchemy_repositories.messages import (
    SqlAlchemyMessageRepository,
)
from chat_realtime_api.infra.sqlalchemy_repositories.rooms import (
    SqlAlchemyRoomRepository,
)
from chat_realtime_api.services.messages.create import (
    CreateMessageInput,
    CreateMessageService,
)


async def chatroom_ws_receiver(
    websocket: WebSocket,
    channel: str,
    service: CreateMessageService,
    current_user: Dict,
):
    async for content in websocket.iter_text():
        try:
            message = service.execute(
                CreateMessageInput(
                    room_id=channel,
                    content=content,
                    user_id=current_user['uid'],
                )
            )
        except Exception as e:
            print(e)
            raise handle_error(e)

        await broadcast.publish(channel=channel, message=message.content)


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
    """
    TODO: O que falta fazer:
        - Carregar as mensagens do banco de dados (Histórico)
        - Enviar as mensagens para usuários que entrarem na sala
        - Tratar erros, para informar o usuário
    """

    current_user = await get_current_user_ws(websocket)

    room_repo = SqlAlchemyRoomRepository(session)
    msg_repo = SqlAlchemyMessageRepository(session)
    service = CreateMessageService(msg_repo, room_repo)

    room_id_str = str(room_id)
    await websocket.accept()

    async with anyio.create_task_group() as task_group:

        async def run_chatroom_ws_receiver() -> None:
            await chatroom_ws_receiver(
                websocket, room_id_str, service, current_user
            )
            task_group.cancel_scope.cancel()

        task_group.start_soon(run_chatroom_ws_receiver)
        await chatroom_ws_sender(websocket, room_id_str)
