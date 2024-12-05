from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MessageSchema(BaseModel):
    id: UUID
    user_id: UUID
    content: str
    timestamp: datetime


class PaginationSchema(BaseModel):
    current_page: int
    page_size: int
    total_pages: int
    total_messages: int


class HistorySchema(BaseModel):
    room_id: UUID
    messages: list[MessageSchema]
    pagination: PaginationSchema
