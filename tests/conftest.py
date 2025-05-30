from unittest.mock import patch
import pytest
from app import create_app, db as _db
from config import TestConfig


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    return _db


@pytest.fixture
def mock_geonames():
    with patch('app.services.requests.get') as mock:
        yield mock


@pytest.fixture
def mock_openmeteo():
    with patch('app.services.requests.get') as mock:
        yield mock
