from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from chat_realtime_api.infra.models.messages import MessageModel
from chat_realtime_api.repositories.messages import (
    HistoryRepoOutput,
    MessageRepoInput,
    MessageRepoOutput,
    MessageRepository,
)


class SqlAlchemyMessageRepository(MessageRepository):
    def __init__(self, session: Session):
        self._session = session

    def save(self, msg_input: MessageRepoInput) -> MessageRepoOutput:
        message_db = MessageModel(
            id=uuid4(),
            room_id=msg_input.room_id,
            content=msg_input.content,
            user_id=msg_input.user_id,
            timestamp=msg_input.timestamp,
        )

        self._session.add(message_db)
        self._session.commit()
        self._session.refresh(message_db)

        return MessageRepoOutput(
            id=message_db.id,
            room_id=message_db.room_id,
            user_id=message_db.user_id,
            content=message_db.content,
            timestamp=message_db.timestamp,
        )

    def get_history_by_room_id(
        self, room_id: UUID, page: int, size: int
    ) -> HistoryRepoOutput:
        messages_db = self._session.scalars(
            select(MessageModel)
            .filter(MessageModel.room_id == room_id)
            .offset((page - 1) * size)
            .limit(size)
        ).all()

        if not messages_db:
            return HistoryRepoOutput(
                room_id=room_id,
                messages=[],
                current_page=page,
                page_size=size,
                total_pages=0,
                total_messages=0,
            )

        total_messages = self._session.scalars(
            select(MessageModel)
            .filter(MessageModel.room_id == room_id)
            .count()
        )

        return HistoryRepoOutput(
            room_id=room_id,
            messages=[
                MessageRepoOutput(
                    id=msg_db.id,
                    room_id=msg_db.room_id,
                    user_id=msg_db.user_id,
                    content=msg_db.content,
                    timestamp=msg_db.timestamp,
                )
                for msg_db in messages_db
            ],
            current_page=page,
            page_size=size,
            total_pages=(total_messages // size) + 1,
            total_messages=total_messages,
        )