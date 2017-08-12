import os

from flask import send_from_directory

from back.app import app


static_dir = os.path.normpath(os.path.join(__file__, '../../front'))


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    if os.path.splitext(path)[1]:
        return send_from_directory(static_dir, path)
    return send_from_directory(static_dir, 'index.html')


@app.route('/', methods=['GET'])
def redirect_to_index():
    return send_from_directory(static_dir, 'index.html')


