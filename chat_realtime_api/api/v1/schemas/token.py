from uuid import UUID

from pydantic import BaseModel


class TokenOutputSchema(BaseModel):
    id: UUID
    name: str
    username: str
    access_token: str
    token_type: str
