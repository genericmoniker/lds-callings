from flask import Flask

from application.database import Database
from application.log import setup_logging, banner

app = None
db = None


def create_app():
    global app, db
    app = Flask(__name__)
    setup_logging(app.logger)
    banner(app.logger, ' web ')
    db = Database()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()
