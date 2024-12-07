from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from chat_realtime_api.api.v1.routers.rooms import router as rooms_router
from chat_realtime_api.api.v1.routers.token import router as token_router
from chat_realtime_api.api.v1.routers.users import router as users_router
from chat_realtime_api.infra.config.security import get_password_hash
from chat_realtime_api.infra.db.session import get_session
from chat_realtime_api.infra.models.base import table_registry
from chat_realtime_api.infra.models.users import UserModel


@pytest.fixture
def token(client, user):
    response = client.post(
        '/api/v1/auth/login',
        data={'username': user.username, 'password': user.clean_password},
    )
    return response.json()['access_token']


@pytest.fixture
def user(session):
    password = 'testtest'
    user = UserModel(
        messages=[],
        name='Teste',
        username='teste@test.com',
        password=get_password_hash(password),
        id=uuid4(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    def create_app():
        app = FastAPI()

        app.include_router(users_router)
        app.include_router(token_router)
        app.include_router(rooms_router)

        return app

    app = create_app()

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
