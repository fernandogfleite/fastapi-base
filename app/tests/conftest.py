import pytest
from starlette.testclient import TestClient

from app.main import create_application


@pytest.fixture
def test_app():
    app = create_application()
    yield app


@pytest.fixture
def test_client(test_app):
    with TestClient(test_app) as client:
        yield client
