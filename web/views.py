import os

from flask import g, send_from_directory, request, jsonify
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import abort

from application.tenant import activate_tenant
from web.app import app, db
from web.user import user_login, verify_auth_token

static_dir = os.path.normpath(os.path.join(__file__, '../../front'))
auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    user = verify_auth_token(token)
    if user:
        g.current_user = user
        activate_tenant(db, user.tenant)
        return True
    return False


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        abort(400, 'Credentials required')
    username = data.get('username')
    password = data.get('password')
    token = user_login(username, password)
    return jsonify({'token': token.decode('ascii')})


@app.route('/api/callings')
@auth.login_required
def callings():
    return jsonify({})


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    if os.path.splitext(path)[1]:
        return send_from_directory(static_dir, path)
    return send_from_directory(static_dir, 'index.html')


@app.route('/', methods=['GET'])
def redirect_to_index():
    return send_from_directory(static_dir, 'index.html')
