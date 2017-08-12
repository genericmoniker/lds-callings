from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from back.log import setup_logging, banner

app = Flask(__name__)
app.config.from_object('back.config')
setup_logging(app.logger)
banner(app.logger, ' web ')
db = SQLAlchemy(app)

# Imports to ensure the web application is set up:
import back.views
import back.models


# Debugging entry point -- in production we run through gunicorn.
if __name__ == "__main__":
    app.run()
