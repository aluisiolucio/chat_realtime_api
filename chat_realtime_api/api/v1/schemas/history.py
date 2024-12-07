from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PaginationQuerySchema(BaseModel):
    page: int = 1
    size: int = 10


class UserSchema(BaseModel):
    id: UUID
    name: str


class MessageSchema(BaseModel):
    id: UUID
    room_id: UUID
    user: UserSchema
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
