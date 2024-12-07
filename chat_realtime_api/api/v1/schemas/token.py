from uuid import UUID

from pydantic import BaseModel


class QueryParams(BaseModel):
    token: str


class TokenOutputSchema(BaseModel):
    id: UUID
    name: str
    username: str
    access_token: str
    token_type: str
