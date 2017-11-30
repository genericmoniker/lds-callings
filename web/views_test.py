import json
import os
import pytest
from unittest import mock

from web.app import create_app

os.environ['SECRET_KEY'] = 'top secret!'
os.environ['DATABASE_URL'] = 'postgres:///lds-callings-test'
create_app()

# Add views to the app after creating it...
import web.views

# http://flask.pocoo.org/docs/0.12/testing/


class JSONFriendlyClient:
    """Wrapper around the Flask test client providing easier JSON support."""

    def __init__(self, flask_test_client):
        self._client = flask_test_client

    def post(self, *args, **kwargs):
        json_data = kwargs.pop('json', None)
        if json_data:
            kwargs['data'] = json.dumps(json_data)
            kwargs['content_type'] = 'application/json'
        return self._client.post(*args, **kwargs)

    def __getattr__(self, item):
        return getattr(self._client, item)


@pytest.fixture(name='db_')
def web_views_db(db):
    web.views.db = db
    yield db


@pytest.fixture(name='client')
def client_fixture():
    yield JSONFriendlyClient(web.views.app.test_client())


VALID_USER_DETAIL = dict(homeUnitNbr='123', individualId='555', units=[
    dict(localUnits=[
        dict(unitNo='123', hasUnitAdminRights=True)
    ])
])


def test_unauthorized(client):
    r = client.get('/api/callings')
    assert r.status_code == 401


@mock.patch('web.user.lds.login')
@mock.patch('web.user.synchronize_async')
def test_login(_mock_sync, mock_login, client, db):
    mock_login.return_value = mock.MagicMock(), VALID_USER_DETAIL
    r = client.post('/api/login', json={'username': 'u', 'password': 'p'})
    assert r.status_code == 200
    token = json.loads(r.data)['token']
    headers = dict(Authorization='Bearer ' + token)
    r = client.get('/api/callings', headers=headers)
    assert r.status_code == 200
