import pytest
from fastapi.testclient import TestClient

from chat_realtime_api.app import app


@pytest.fixture
def client():
    return TestClient(app)
