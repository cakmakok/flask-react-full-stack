import pytest

from backend.src.main import \
    app as flask_app,\
    db as flask_db

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db():
    yield flask_db
