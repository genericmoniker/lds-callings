import pytest
from copy import deepcopy
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden
from unittest import mock

import web.app
import web.user
from application.lds import AuthenticationError
from application.models import User
from web.user import user_login


@pytest.fixture(name='db_')
def web_user_db(db):
    web.user.db = db
    yield db


USER_DETAIL = {
    'individualId': 1231231231,
    'homeUnitNbr': 300,
    'units': [
        {
            'unitName': 'A Stake',
            'unitNo': 500,
            'orgTypeId': 5,
            'hasUnitAdminRights': False,
            'hasUnitPhotoAdminRights': False,
            'hasCallingInUnit': False,
            'localUnits': [
                {
                    'unitName': 'A Ward',
                    'unitNo': 300,
                    'orgTypeId': 7,
                    'hasUnitAdminRights': True,
                    'hasUnitPhotoAdminRights': True,
                    'hasCallingInUnit': True
                },
            ]
        }
    ],
    'memberAssignments': [
        {
            'positionTypeId': 57,
            'unitNo': 300,
            'organizationTypeId': 7
        }
    ]
}


def test_error_when_missing_username():
    with pytest.raises(BadRequest):
        user_login(username='', password='p')


def test_error_when_missing_password():
    with pytest.raises(BadRequest):
        user_login(username='u', password='')


@mock.patch('web.user.lds.login')
def test_error_with_bad_credentials(mock_login):
    mock_login.side_effect = AuthenticationError
    with pytest.raises(Unauthorized):
        user_login('u', 'p')


@mock.patch('web.user.lds.login')
def test_error_with_unauthorized_user(mock_login):
    s = mock.MagicMock()
    detail = deepcopy(USER_DETAIL)
    detail['units'][0]['localUnits'][0]['hasUnitAdminRights'] = False
    mock_login.return_value = s, detail
    with pytest.raises(Forbidden):
        user_login('u', 'p')


@mock.patch('web.user.lds.login')
@mock.patch('web.user.ensure_tenant')
@mock.patch('web.user.synchronize_async')
def test_tenant_established_on_login(_mock_sync, mock_tenant, mock_login, db_):
    mock_login.return_value = mock.MagicMock(), deepcopy(USER_DETAIL)
    user_login('u', 'p')
    assert mock_tenant.called


@mock.patch('web.user.lds.login')
@mock.patch('web.user.ensure_tenant')
@mock.patch('web.user.synchronize_async')
def test_create_user_on_first_login(_mock_sync, mock_tenant, mock_login, db_):
    mock_login.return_value = (mock.MagicMock(), deepcopy(USER_DETAIL))
    assert db_.session.query(User).count() == 0
    user_login('u', 'p')
    assert db_.session.query(User).count() == 1


@mock.patch('web.user.lds.login')
@mock.patch('web.user.ensure_tenant')
@mock.patch('web.user.synchronize_async')
def test_reuse_user_on_later_login(_mock_sync, mock_tenant, mock_login, db_):
    detail = deepcopy(USER_DETAIL)
    mock_login.return_value = (mock.MagicMock(), detail)
    db_.session.add(User(id=detail['individualId'], unit=detail['homeUnitNbr']))
    user_login('u', 'p')
    assert db_.session.query(User).count() == 1
