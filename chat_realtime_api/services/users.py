from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from chat_realtime_api.infra.config.security import get_password_hash
from chat_realtime_api.repositories.users import (
    UserRepoInput,
    UserRepository,
)
from chat_realtime_api.services.errors.exceptions import (
    UserAlreadyExistsException,
)


@dataclass
class CreateUserInput:
    username: str
    password: str


@dataclass
class CreateUserOutput:
    id: UUID
    username: str
    access_token: Optional[str] = None
    token_type: Optional[str] = None


class CreateUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, input: CreateUserInput) -> CreateUserOutput:
        hashed_password = get_password_hash(input.password)

        user_input = UserRepoInput(
            username=input.username,
            password=hashed_password,
        )

        user_output = self.repository.save(user_input)

        if isinstance(user_output, str):
            raise UserAlreadyExistsException(user_input.username)

        return CreateUserOutput(
            id=user_output.id,
            username=user_output.username,
        )
