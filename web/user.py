import logging
import uuid

from werkzeug.exceptions import abort

from application import lds
from application.models import User
from application.tenant import ensure_tenant
from web.app import db
from web.jobs import synchronize_async

logger = logging.getLogger(__name__)


def generate_auth_token(expires_in=600):
    return uuid.uuid4()  # TODO


def verify_auth_token(token):
    return None  # TODO - if valid, return the user


def user_login(username, password):
    if not (username and password):
        abort(400, 'Missing username or password.')
    s = detail = None  # keep lint happy
    try:
        s, detail = lds.login(username, password)
    except lds.AuthenticationError:
        logger.info(f'Failed login attempt for user: {username}')
        abort(401, 'Incorrect username or password.')
    if not user_is_authorized(detail):
        logger.info(f'Unauthorized login attempt for user: {username}')
        abort(403, 'Not authorized.')
    logger.info(f'Successful login for user: {username}')
    unit = detail['homeUnitNbr']
    ensure_tenant(db, unit)
    id_ = detail['individualId']
    user = db.session.query(User).get(id_)
    if not user:
        user = User(id=id_, unit=unit)
        db.session.add(user)
        db.session.commit()
    synchronize_async.delay(s, unit)


def user_is_authorized(user_detail):
    unit_number = user_detail['homeUnitNbr']
    for unit in user_detail['units'][0]['localUnits']:
        if unit['unitNo'] == unit_number:
            return unit['hasUnitAdminRights']
