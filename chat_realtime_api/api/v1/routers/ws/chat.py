from contextlib import asynccontextmanager
from typing import Annotated, Dict, List
from uuid import UUID

import anyio
from broadcaster import Broadcast
from fastapi import (
    APIRouter,
    Depends,
    Query,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from chat_realtime_api.api.v1.errors.error_handlers import handle_error
from chat_realtime_api.api.v1.schemas.token import QueryParams
from chat_realtime_api.infra.config.security import (
    get_current_user,
    get_current_user_ws,
)
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
from chat_realtime_api.services.messages.get import GetMessageService


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
        self, room_id: str, message, exclude: List[WebSocket] = None
    ):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                if exclude and connection in exclude:
                    continue

                try:
                    if isinstance(message, str):
                        await connection.send_json({'content': message})
                    else:
                        await connection.send_json({
                            'content': message.content,
                            'timestamp': message.timestamp.strftime(
                                '%Y-%m-%d %H:%M:%S'
                            ),
                        })
                except Exception:
                    self.disconnect(room_id, connection)


manager = ConnectionManager()
broadcast = Broadcast(Settings().DATABASE_URL)


async def chatroom_ws_receiver(
    websocket: WebSocket,
    channel: str,
    service: CreateMessageService,
    current_user: Dict,
):
    async for message in websocket.iter_json():
        if not isinstance(message, dict) or 'content' not in message:
            await websocket.send_json({'error': 'Invalid message format.'})
            continue

        try:
            msg = service.execute(
                CreateMessageInput(
                    room_id=channel,
                    content=message['content'],
                    user_id=current_user['uid'],
                )
            )
        except Exception as e:
            print(e)
            raise handle_error(e)

        await broadcast.publish(
            channel=channel,
            message=msg.content,
        )


async def chatroom_ws_sender(websocket: WebSocket, room_id: str):
    async with broadcast.subscribe(channel=room_id) as subscriber:
        async for event in subscriber:
            await websocket.send_json({
                'content': event.message,
            })


@asynccontextmanager
async def lifespan(app):
    await broadcast.connect()
    try:
        yield
    finally:
        await broadcast.disconnect()


router = APIRouter(prefix='/api/v1', tags=['chat'], lifespan=lifespan)


@router.get('/chat', response_class=HTMLResponse)
async def get_index():
    with open('index.html', 'r', encoding='utf-8') as file:
        return HTMLResponse(content=file.read())


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
        f'User {current_user["name"]} joined the chat.',
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
        await websocket.send_json({'error': 'Error fetching messages.'})

    try:
        async with anyio.create_task_group() as task_group:

            async def run_chatroom_ws_receiver() -> None:
                await chatroom_ws_receiver(
                    websocket, room_id_str, create_service, current_user
                )
                task_group.cancel_scope.cancel()

            task_group.start_soon(run_chatroom_ws_receiver)
            await chatroom_ws_sender(websocket, room_id_str)
    except WebSocketDisconnect:
        manager.disconnect(room_id_str, websocket)
        await manager.broadcast(
            room_id_str, f'User {current_user["name"]} has left the chat.'
        )


@router.get(
    '/chat/{room_id}',
    include_in_schema=True,
    summary='WebSocket Documentation',
)
def websocket_docs(
    room_id: str,
    pagination_query_schema: Annotated[QueryParams, Query()],
    current_user: Dict = Depends(get_current_user),
):
    """
    **WebSocket Endpoint**

    Use este endpoint para se conectar ao chat via WebSocket.

    **URL:** `ws://localhost:8000/chat/{room_id}`

    **Parâmetros:**
    - `room_id`: O ID da sala de chat.

    **Query Parameters:**
    - `token`: Token JWT no formato `Bearer <token>`
    """
    return JSONResponse({
        'detail': 'Use WebSocket em ws://localhost:8000/chat/{room_id}'
    })
