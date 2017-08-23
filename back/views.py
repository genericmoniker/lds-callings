import os

from flask import abort, g, send_from_directory, request, jsonify
from flask_httpauth import HTTPTokenAuth

from back.app import app, db
from back import lds
from back.models import User
from back.tenant import ensure_tenant, activate_tenant

static_dir = os.path.normpath(os.path.join(__file__, '../../front'))
auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if user:
        g.current_user = user
        activate_tenant(user)
        return True
    return False


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not (username and password):
        abort(400, 'Missing username or password.')
    s = None  # lint
    try:
        s = lds.login(username, password)
    except lds.AuthenticationError:
        app.logger.info(f'Failed login attempt for user: {username}')
        abort(401, 'Incorrect username or password.')
    detail = lds.fetch_current_user_detail(s)
    if not user_is_authorized(detail):
        abort(403, 'Not authorized.')
    app.logger.info(f'Successful login for user: {username}')
    unit = detail['homeUnitNbr']
    ensure_tenant(unit)
    id_ = detail['individualId']
    user = User.query.get(id_)
    if not user:
        user = User(id=id_, unit=unit)
        db.session.add(user)
        db.session.commit()
    return jsonify({'token': user.generate_auth_token()})


def user_is_authorized(user_detail):
    unit_number = user_detail['homeUnitNbr']
    for unit in user_detail['units'][0]['localUnits']:
        if unit['unitNo'] == unit_number:
            return unit['hasUnitAdminRights']


@app.route('/api/callings')
@auth.login_required
def callings():
    return {}


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    if os.path.splitext(path)[1]:
        return send_from_directory(static_dir, path)
    return send_from_directory(static_dir, 'index.html')


@app.route('/', methods=['GET'])
def redirect_to_index():
    return send_from_directory(static_dir, 'index.html')
