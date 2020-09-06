import pytest

from backend.src.main import app as flask_app
from backend.src.main import db as flask_db
from backend.src.main import Broker


@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db():
    yield flask_db

@pytest.fixture
def all_brokers():
    return Broker.query.all()
