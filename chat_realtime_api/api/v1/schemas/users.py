from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserInputSchema(BaseModel):
    username: EmailStr
    password: Optional[str] = None


class UserOutputSchema(BaseModel):
    id: UUID
    username: EmailStr
