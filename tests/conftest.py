import json
import pytest

from app import create_app

@pytest.yield_fixture(scope='session')
def flask_app():

    app = create_app('app.config.Test')
    from app.database.db import db

    with app.app_context():
        db.init_app(app)
        db.create_all()
        yield app

@pytest.fixture(scope='session')
def client(flask_app):
    return flask_app.test_client()