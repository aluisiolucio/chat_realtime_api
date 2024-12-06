from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserInputSchema(BaseModel):
    name: str
    username: EmailStr
    password: Optional[str] = None


class UserOutputSchema(BaseModel):
    id: UUID
    name: str
    username: EmailStr
