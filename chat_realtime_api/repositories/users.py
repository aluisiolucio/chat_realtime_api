from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserRepoInput:
    name: str
    username: str
    password: str


@dataclass
class UserRepoOutput:
    id: UUID
    name: str
    username: str
    password: str | None = None


class UserRepository:
    def save(self, user_input: UserRepoInput) -> UserRepoOutput | str:
        raise NotImplementedError

    def get_by_username(self, username: str) -> UserRepoOutput | None:
        raise NotImplementedError
