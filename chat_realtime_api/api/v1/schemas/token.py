from uuid import UUID

from pydantic import BaseModel


class TokenOutputSchema(BaseModel):
    id: UUID
    username: str
    access_token: str
    token_type: str
