from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from chat_realtime_api.infra.config.security import (
    create_access_token,
    verify_password,
)
from chat_realtime_api.repositories.users import UserRepository
from chat_realtime_api.services.errors.exceptions import (
    InvalidCredentialsException,
    UserNotFoundException,
)


@dataclass
class TokenInput:
    username: str
    password: str


@dataclass
class TokenOutput:
    id: UUID
    username: str
    access_token: Optional[str] = None
    token_type: Optional[str] = None


class Token:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, input: TokenInput) -> TokenOutput:
        user = self.repository.get_by_username(input.username)

        if not user:
            raise UserNotFoundException(input.username)

        if not verify_password(input.password, user.password):
            raise InvalidCredentialsException()

        access_token = create_access_token(
            data={
                'uid': str(user.id),
                'sub': user.username,
            }
        )

        return TokenOutput(
            id=user.id,
            username=user.username,
            access_token=access_token,
            token_type='bearer',
        )


class RefreshToken:
    @staticmethod
    def execute(id: UUID, username: str) -> TokenOutput:
        access_token = create_access_token(
            data={
                'uid': str(id),
                'sub': username,
            }
        )

        return TokenOutput(
            id=id,
            username=username,
            access_token=access_token,
            token_type='bearer',
        )
