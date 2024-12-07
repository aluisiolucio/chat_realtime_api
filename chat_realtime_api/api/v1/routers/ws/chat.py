from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
from uuid import UUID

import anyio
from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from sqlalchemy.orm import Session

from chat_realtime_api.api.v1.errors.error_handlers import handle_error
from chat_realtime_api.infra.config.security import (
    get_current_user_ws,
)
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
from chat_realtime_api.services.messages.get import GetMessageService


@dataclass
class Message:
    content: str
    user: str
    timestamp: datetime


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
        await websocket.accept()

    def disconnect(self, room_id: str, websocket: WebSocket):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(
        self, room_id: str, message: Message, exclude: List[WebSocket] = None
    ):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                if exclude and connection in exclude:
                    continue

                try:
                    await connection.send_json({
                        'content': message.content,
                        'user': message.user,
                        'timestamp': message.timestamp.strftime(
                            '%Y-%m-%d %H:%M:%S'
                        ),
                    })
                except Exception as e:
                    print(e)
                    self.disconnect(room_id, connection)


manager = ConnectionManager()

router = APIRouter(prefix='/api/v1', tags=['chat'])


@router.websocket('/chat/{room_id}')
async def chat_websocket(
    websocket: WebSocket,
    room_id: UUID,
    session: Session = Depends(get_session),
):
    try:
        current_user = await get_current_user_ws(websocket)
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    room_repo = SqlAlchemyRoomRepository(session)
    msg_repo = SqlAlchemyMessageRepository(session)

    create_service = CreateMessageService(msg_repo, room_repo)
    get_service = GetMessageService(msg_repo, room_repo)

    room_id_str = str(room_id)
    await manager.connect(room_id_str, websocket)

    await manager.broadcast(
        room_id_str,
        message=Message(
            content=f'User {current_user["name"]} has joined the chat.',
            user=current_user['name'],
            timestamp=datetime.now(),
        ),
        exclude=[websocket],
    )

    try:
        messages = get_service.execute(room_id)
        for msg in reversed(messages):
            await websocket.send_json({
                'content': msg.content,
                'user': msg.user.name,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            })
    except Exception as e:
        print(e)
        await websocket.send_json({'error': str(e)})
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        async with anyio.create_task_group() as task_group:

            async def run_chatroom_ws_receiver() -> None:
                async for message in websocket.iter_json():
                    if (
                        not isinstance(message, dict)
                        or 'content' not in message
                    ):
                        await websocket.send_json({
                            'error': 'Invalid message format.'
                        })
                        continue

                    try:
                        msg = create_service.execute(
                            CreateMessageInput(
                                room_id=room_id_str,
                                content=message['content'],
                                user_id=current_user['uid'],
                            )
                        )

                        await manager.broadcast(
                            room_id_str,
                            message=Message(
                                content=msg.content,
                                user=current_user['name'],
                                timestamp=msg.timestamp,
                            ),
                            exclude=[websocket],
                        )
                    except Exception as e:
                        print(e)
                        raise handle_error(e)

                task_group.cancel_scope.cancel()

            task_group.start_soon(run_chatroom_ws_receiver)
    except WebSocketDisconnect:
        manager.disconnect(room_id_str, websocket)
        await manager.broadcast(
            room_id_str,
            message=Message(
                content=f'User {current_user["name"]} has left the chat.',
                user=current_user['name'],
                timestamp=datetime.now(),
            ),
            exclude=[websocket],
        )
