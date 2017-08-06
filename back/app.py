import logging

import os
from flask import Flask, send_from_directory

logger = logging.getLogger(__name__)
logger.info(' startup '.center(50, '='))

static_dir = os.path.normpath(os.path.join(__file__, '../../front'))

app = Flask(__name__)


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    if os.path.splitext(path)[1]:
        return send_from_directory(static_dir, path)
    return send_from_directory(static_dir, 'index.html')


@app.route('/', methods=['GET'])
def redirect_to_index():
    return send_from_directory(static_dir, 'index.html')


if __name__ == "__main__":
    app.run()
