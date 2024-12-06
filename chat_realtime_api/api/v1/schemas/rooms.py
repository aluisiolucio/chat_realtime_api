from uuid import UUID

from pydantic import BaseModel


class RoomInputSchema(BaseModel):
    name: str
    description: str | None = None


class RoomOutputSchema(BaseModel):
    id: UUID
    name: str
    creator_id: UUID
    description: str | None = None


class ListRoomOutputSchema(BaseModel):
    rooms: list[RoomOutputSchema]
