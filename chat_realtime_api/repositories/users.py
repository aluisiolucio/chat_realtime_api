from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class UserRepoInput:
    username: str
    password: str


@dataclass
class UserRepoOutput:
    id: UUID
    username: str
    password: Optional[str] = None


class UserRepository:
    def save(self, user_input: UserRepoInput) -> UserRepoOutput | str:
        raise NotImplementedError

    def get_by_username(self, username: str) -> UserRepoOutput | None:
        raise NotImplementedError
