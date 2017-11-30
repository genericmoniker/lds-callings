import logging

from werkzeug.exceptions import abort
from itsdangerous import TimedJSONWebSignatureSerializer as JWT

from application import lds
from application.models import User
from application.tenant import ensure_tenant
from web.app import app, db
from web.jobs import synchronize_async

logger = logging.getLogger(__name__)

_jwt_serializer_instance = None


def _jwt_serializer():
    global _jwt_serializer_instance
    if _jwt_serializer_instance is None:
        _jwt_serializer_instance = JWT(app.config['SECRET_KEY'], 2 * 60 * 60)
    return _jwt_serializer_instance


def generate_auth_token(user):
    return _jwt_serializer().dumps({'user_id': user.id})


def verify_auth_token(token):
    try:
        user_id = _jwt_serializer().loads(token)['user_id']
        return db.session.query(User).get(user_id)
    except Exception:
        return None


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
    return generate_auth_token(user)


def user_is_authorized(user_detail):
    """Determine if a user is authorized to use this application."""
    unit_number = user_detail['homeUnitNbr']
    for unit in user_detail['units'][0]['localUnits']:
        if unit['unitNo'] == unit_number:
            return unit['hasUnitAdminRights']
