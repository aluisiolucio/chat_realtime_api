from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from chat_realtime_api.infra.models.users import UserModel
from chat_realtime_api.repositories.users import (
    UserRepoInput,
    UserRepoOutput,
    UserRepository,
)


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self._session = session

    def save(self, user_input: UserRepoInput) -> UserRepoOutput | str:
        user_db = self._session.scalar(
            select(UserModel).where(UserModel.username == user_input.username)
        )

        if user_db:
            return 'User already exists'

        user_db = UserModel(
            id=uuid4(),
            name=user_input.name,
            username=user_input.username,
            password=user_input.password,
        )

        self._session.add(user_db)
        self._session.commit()
        self._session.refresh(user_db)

        return UserRepoOutput(
            id=user_db.id,
            name=user_db.name,
            username=user_db.username,
        )

    def get_by_username(self, username: str) -> UserRepoOutput | None:
        user_db = self._session.scalar(
            select(UserModel).where(UserModel.username == username)
        )

        if not user_db:
            return None

        return UserRepoOutput(
            id=user_db.id,
            name=user_db.name,
            username=user_db.username,
            password=user_db.password,
        )
